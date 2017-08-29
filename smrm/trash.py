import os
import sys
import json
import shutil
import time
import re
import logging
from .utils import confirmed, get_size, conflict_solver, output, Progress, ExitCodes, get_list_of_directories
import multiprocessing
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class Trash(object):
    def __init__(self, trash_path, current_directory=os.getcwd(), storage_time=False,
                 trash_maximum_size=False, recover_conflict='not_replace',
                 interactive=False, log_path=os.getcwd() + "/log", dry_run=False, force=False):

        self.trash_path = trash_path
        self.current_directory = current_directory
        self.storage_time = storage_time
        self.trash_maximum_size = trash_maximum_size
        self.recover_conflict = recover_conflict
        self.interactive = interactive
        self.dry_run = dry_run
        self.force = force
        self.filelist_path = os.path.join(self.trash_path, 'filelist')
        if not os.path.exists(self.trash_path):
            os.mkdir(self.trash_path)

        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filemode="w",
                            filename=log_path, level=logging.DEBUG)
        logging.info("Trash path {}".format(trash_path))

    def __load_from_filelist(self):
        with open(self.filelist_path, 'a+') as filelist:
            try:
                self.filelist_dict = json.load(filelist)
            except ValueError:
                self.filelist_dict = {}

    def __save_to_filelist(self):
        with open(self.filelist_path, 'w+') as filelist:
            filelist.write(json.dumps(self.filelist_dict))

    def mover_to_trash(self, filepath):
        filepath_in_trash = os.path.join(self.trash_path, str(os.stat(filepath).st_ino))
        try:
            os.rename(filepath, filepath_in_trash)
        except OSError:
            return ExitCodes.UNKNOWN, filepath_in_trash, filepath
        else:
            return ExitCodes.GOOD, filepath_in_trash, filepath

    def delete_to_trash(self, target, is_multiprocessing=False):
        info_message = ''
        exit_code = ExitCodes.GOOD
        filepath = os.path.abspath(target)
        if os.path.exists(filepath) or self.force:
            if not self.interactive or confirmed(target):
                if os.access(filepath, os.W_OK):
                    if not self.dry_run:
                        exit_code, filepath_in_trash, filepath = self.mover_to_trash(filepath)

                        if not is_multiprocessing:
                            self.__load_from_filelist()
                            self.filelist_dict[filepath_in_trash] = filepath
                            self.__save_to_filelist()

                        if exit_code == ExitCodes.GOOD:
                            info_message = target + ' moved to trash'
                        else:
                            info_message = "Unknown error"
                    else:
                        info_message = target + ' wil be moved to trash'
                else:
                    info_message = target + " not exists or no access to it"
                    exit_code = ExitCodes.UNKNOWN
            else:
                info_message = target + " - deleting canceled"
        else:
            info_message = target + " not exists"
            exit_code = ExitCodes.NO_FILE
        if self.force:
            exit_code = ExitCodes.GOOD
            info_message = ""
        if exit_code != ExitCodes.GOOD:
            logging.error(info_message)
        else:
            logging.info(info_message)
        if is_multiprocessing:
            return info_message, filepath_in_trash, filepath
        else:
            return info_message, exit_code

    def get_last_deleted(self, recover_list):
        oldest_file = recover_list[0]
        j = 0
        for i in range(len(recover_list)):
            if os.path.getctime(recover_list[i][0]) > os.path.getctime(oldest_file[0]):
                oldest_file = recover_list[i]
                j = i
        return j

    def mover_from_trash(self, filepath_in_trash, filepath):
        info_message = ''
        exit_code = ExitCodes.GOOD

        if os.path.exists(filepath):
            exit_code = ExitCodes.CONFLICT
            if self.recover_conflict != 'replace':
                while os.path.exists(filepath):
                    filepath = conflict_solver(filepath)

        if not self.dry_run:
            try:
                os.rename(filepath_in_trash, filepath)
            except OSError:
                info_message = 'Something go wrong while renaming'
                exit_code = ExitCodes.UNKNOWN
                logging.error(info_message)
            else:
                self.filelist_dict.pop(filepath_in_trash)
                info_message = "Recovered " + os.path.basename(filepath)
                logging.info(info_message)
        else:
            info_message = os.path.basename(filepath) + " will be recovered"

        self.__save_to_filelist()
        return info_message, exit_code

    def recover_from_trash(self, target):
        self.__load_from_filelist()

        # getting [(path in trash, original path of file)]
        recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == target]

        if len(recover_list) == 0:
            info_message = "There is no {} in trash".format(target)
            exit_code = ExitCodes.NO_FILE
            logging.error(info_message)

        elif len(recover_list) == 1:
            info_message, exit_code = self.mover_from_trash(recover_list[0][0], recover_list[0][1])
        else:
            i = int(self.get_last_deleted(recover_list))  # for auto recover
            info_message, exit_code = self.mover_from_trash(recover_list[i][0], recover_list[i][1])

        return info_message, exit_code

    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_path)
            os.mkdir(self.trash_path)
            logging.info("Trash wiped")
            return "Trash wiped", 0
        else:
            return "Trash will be wiped", 0

    def show_trash(self, n=0):
        self.__load_from_filelist()
        return_list = []

        if self.filelist_dict != {}:
            filelist = [item for item in self.filelist_dict.items()[-n:]]
            for i in range(len(filelist)):
                return_list.append(('"{0}" deleted from {1} at {2}'.format(os.path.basename(filelist[i][1]),
                                                                           os.path.split(filelist[i][1])[0],
                                                                           time.ctime(
                                                                               os.path.getctime(filelist[i][0]))), 0,
                                    filelist[i][0], filelist[i][1]))

        else:
            logging.info("Trash is empty")
        return return_list

    def delete_trash(self):
        if os.path.exists(self.trash_path):
            shutil.rmtree(self.trash_path)

    def policy_check(self):
        self.__load_from_filelist()

        if self.storage_time:
            for f in self.filelist_dict.keys():
                if (time.time() - os.path.getctime(f)) > self.storage_time * 86400:  # 86400 = sec in day
                    if not os.path.isdir(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
                    self.filelist_dict.pop(f)

                    self.__save_to_filelist()

        if self.trash_maximum_size:
            while get_size(self.trash_path) > self.trash_maximum_size:
                try:
                    oldest_file = self.filelist_dict.keys()[0]
                except IndexError:
                    break
                for f in self.filelist_dict.keys():
                    if os.path.getctime(f) > os.path.getctime(oldest_file):
                        oldest_file = f

                self.filelist_dict.pop(oldest_file)
                logging.info("Policy: deleted " + oldest_file)
                if not os.path.isdir(oldest_file):
                    os.remove(oldest_file)
                else:
                    shutil.rmtree(oldest_file)

        self.__save_to_filelist()

    def reg(self, directory, regular, mp_dict, return_list):
        for f in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, f)):
                if re.match(regular, f):
                    info_message, filepath_in_trash, filepath = self.delete_to_trash(os.path.join(directory, f),
                                                                                     is_multiprocessing=True)
                    mp_dict[filepath_in_trash] = filepath
                    return_list.append(info_message)

    def delete_to_trash_by_reg(self, regular, directory, return_list=None, silent=False):
        listdir = get_list_of_directories(directory)  # recursive list of directories
        listdir.append(directory)

        mgr = multiprocessing.Manager()
        if return_list is None:
            return_list = mgr.list()
        mp_dict = mgr.dict()
        proc_list = []

        while len(listdir) > 0:
            p = multiprocessing.Process(target=self.reg, args=(listdir.pop(), regular, mp_dict, return_list))
            proc_list.append(p)
            p.start()

        for p in proc_list:
            p.join()

        self.__load_from_filelist()
        self.filelist_dict.update(mp_dict)
        self.__save_to_filelist()
        if len(return_list) == 0:
            if os.path.exists(directory):
                return_list.append("No matches")
            else:
                return_list.append("Directory not exists")
        return return_list


        # def delete_to_trash_by_reg2(self, regular, directory, silent=False):
        #     progress = Progress(os.path.abspath(directory))
        #     info_message = ''
        #     exit_code = ExitCodes.GOOD

        #     for path, directories, files in os.walk(directory):
        #         for f in files:
        #             if re.match(regular, f):
        #                 if not self.interactive or confirmed(f):
        #                     progress.inc()
        #                     info_message, exit_code = self.delete_to_trash(os.path.join(path, f))
        #         if not silent:
        #             progress.show()
        #     if not silent:
        #         progress.end()
        #     return "", exit_code
