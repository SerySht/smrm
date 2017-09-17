"""
This module contains class Trash, which serves for creation and manipulation with trashes

Parameters for initializzations of Trash:
    non-optional:
        trash_path = path of trash
    optional:
        trash_maximum_size = maximum size of trash, default = False
        storage_time = time of storaging files(in days), default = False
        recover_conflict = what do if name conflice while restore file (replace/not_replace), default = 'not_replace'
        interactive = turn on interactive mode, default = False
        log_path = path of log file, default = home dir
        silent = turn on silent mode, default = False
        verbose = turn on verbose mode(commenting what is happening), default = False
        dry_run = turn on dry mode (not appling changes), default = False
        force = turn to force mode, default = False


Example of working with Trash:
    my_trash = Trash(trash_path = "/home/username/Trash", verbose=True)
    my_trash.delete_trash("/home/username/file1")
"""
import os
import sys
import json
import re
import logging
from smrm.utils import confirmed, get_size, conflict_solver, output, Progress, ExitCodes
import multiprocessing
import codecs 
import time


class Trash(object):
    """
    Class for creation and manipulation with trash
    """
    def __init__(self, trash_path, trash_maximum_size=False, storage_time=False, 
                    recover_conflict='not_replace', interactive=False,  
                    log_path=os.getcwd() + "/log", silent=False, verbose = False, 
                    dry_run=False, force=False):

        self.trash_path = trash_path   
        self.storage_time = storage_time
        self.trash_maximum_size = trash_maximum_size
        self.recover_conflict = recover_conflict
        self.interactive = interactive
        self.dry_run = dry_run
        self.force = force
        self.filelist_path = os.path.join(self.trash_path, 'filelist')
        self.silent = silent
        self.verbose = verbose
        
        if not os.path.exists(self.trash_path):
            os.mkdir(self.trash_path)
        
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filemode="w",
                             filename=log_path, level=logging.DEBUG)
        logging.info("Trash path {}".format(trash_path))

    
    def _load_from_filelist(self):
        with codecs.open(self.filelist_path, 'a+', encoding='utf-8') as filelist:
            try:
                self.filelist_dict = json.load(filelist)
            except ValueError:
                self.filelist_dict = {}

    
    def _save_to_filelist(self):
        with codecs.open(self.filelist_path, 'w+', encoding='utf-8') as filelist:
            filelist.write(json.dumps(self.filelist_dict))

    
    def _mover_to_trash(self, filepath):
        """Gets path of the file and moves it to the Trash"""
        filepath_in_trash = os.path.join(self.trash_path, str(os.stat(filepath).st_ino))

        # cheking for accesses of all files in directory
        if os.path.isdir(filepath):
            for root, dirs, files in os.walk(filepath):
                for f in dirs + files:  
                    if not os.access(os.path.join(root, f), os.W_OK):
                        return ExitCodes.NO_ACCESS, root, f
        try:    
            os.rename(filepath, filepath_in_trash)
        except OSError:
            return ExitCodes.UNKNOWN, filepath_in_trash, filepath
        else:
            return ExitCodes.GOOD, filepath_in_trash, filepath
    

    def _delete_to_trash(self, target, filelist_dict):  
        """Calls _mover_to_trash and forms exit_code and info_message"""       
        if not isinstance(target, unicode):
            target = target.decode("utf-8")

        exit_code = ExitCodes.GOOD
        filepath = os.path.abspath(target)      

        if os.path.exists(filepath):
            if not self.interactive or confirmed(target):
                if os.access(filepath, os.W_OK):
                    if not self.dry_run:
                        
                        exit_code, filepath_in_trash, filepath = self._mover_to_trash(filepath)
                        
                        if exit_code == ExitCodes.GOOD:
                            filelist_dict[filepath_in_trash] = filepath                        
                            info_message = target + u" moved to trash"                    

                        else:
                            info_message = u"Unknown error"
                            exit_code = ExitCodes.UNKNOWN

                        if exit_code == ExitCodes.NO_ACCESS:
                            info_message = u"Error: No access to {}/{}".format(filepath_in_trash, filepath)  
                    
                    else:
                        info_message = target + u" will be moved to trash"
                else:
                    info_message = target + u" not exists or no access to it"
                    exit_code = ExitCodes.UNKNOWN
            else:
                info_message = target + u" deleting canceled"
                exit_code = ExitCodes.NO_ACCESS
        else:
            if self.force:                
                info_message = u""
            else:
                info_message = target + u" not exists" 
                exit_code = ExitCodes.NO_FILE        
        
        if exit_code != ExitCodes.GOOD:
            logging.error(info_message)
        else:
            logging.info(info_message)
        
        if self.silent:
            info_message = "" 
              
        if exit_code == ExitCodes.GOOD and not self.dry_run and not self.verbose:           
            info_message = ""        
       
        return info_message, exit_code


    def delete_to_trash(self, targets):  
        """Gets target or list of targets and moves it to the trash, using multiprocessing"""        
        if not isinstance(targets, list):
            targets = [targets]

        mgr = multiprocessing.Manager()         
        mp_dict = mgr.dict()         
        
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        return_list = pool.map(_pickled_delete_to_trash, [(self, target, mp_dict) for target in targets])                              
        pool.close()
        pool.join()

        self._load_from_filelist()
        self.filelist_dict.update(mp_dict)
        self._save_to_filelist()
        self.policy_check()                          
       
        return return_list    

    
    def _get_last_deleted(self, recover_list):       
        last_file = recover_list[0]
        j = 0
        for i in range(len(recover_list)):
            if os.path.getctime(recover_list[i][0]) > os.path.getctime(last_file[0]):
                last_file = recover_list[i]
                j = i
        return j


    def mover_from_trash(self, filepath_in_trash, filepath):
        """Gets path of file in trash and original path and replace file to original path"""    
        exit_code = ExitCodes.GOOD

        if os.path.exists(filepath):
            exit_code = ExitCodes.CONFLICT
            if self.recover_conflict != "replace":
                while os.path.exists(filepath):
                    filepath = conflict_solver(filepath)

        if not self.dry_run:
            try:
                os.rename(filepath_in_trash, filepath)
            except OSError:
                info_message = u"Something go wrong while renaming"
                exit_code = ExitCodes.UNKNOWN
                logging.error(info_message)
            else:
                self.filelist_dict.pop(filepath_in_trash)
                info_message = u"Recovered " + os.path.basename(filepath)
                logging.info(info_message)
        else:
            info_message = os.path.basename(filepath) + u" will be recovered"

        self._save_to_filelist()
        return info_message, exit_code


    def recover_from_trash(self, target):
        """Finds suitable files for target in trash_dict and calls mover_from_trash"""        
        if not isinstance(target, unicode):
            target = target.decode("utf-8")
        self._load_from_filelist()

        # getting [(path in trash, original path of file)]
        recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == target]

        if len(recover_list) == 0:
            info_message = "There is no {} in trash".format(target)
            exit_code = ExitCodes.NO_FILE
            logging.error(info_message)

        elif len(recover_list) == 1:
            info_message, exit_code = self.mover_from_trash(recover_list[0][0], recover_list[0][1])
        else:
            i = int(self._get_last_deleted(recover_list))
            info_message, exit_code = self.mover_from_trash(recover_list[i][0], recover_list[i][1])
        self.policy_check()
        return info_message, exit_code

    
    def _delete_directory(self, directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for d in dirs:                
                os.rmdir(os.path.join(root,d))
            for f in files:
                os.remove(os.path.join(root,f))
        os.rmdir(directory)
    
    
    def wipe_trash(self):
        """Cleaning trash directory"""
        if not self.dry_run:
            self._delete_directory(self.trash_path)
            os.mkdir(self.trash_path)            
            logging.info("Trash wiped")
            return [("Trash wiped", ExitCodes.GOOD)]
        else:
            return [("Trash will be wiped", ExitCodes.GOOD)]


    def show_trash(self, n=0):
        """If gets n shows last n files, if no - all content of trash"""
        self._load_from_filelist()
        return_list = []  
        if self.filelist_dict != {}:         
            filelist = [item for item in self.filelist_dict.items()[-n:]]
            for i in range(len(filelist)):
                return_list.append((u'"{0}" deleted from {1} at {2}'.format(os.path.basename(filelist[i][1]),
                                                                            os.path.split(filelist[i][1])[0],
                                                                            time.ctime(os.path.getctime(filelist[i][0]))), 
                                    ExitCodes.GOOD,
                                    filelist[i][0], 
                                    filelist[i][1]))

        else:
            logging.info("Trash is empty")
        return return_list


    def delete_trash(self):
        """Removes trash directory"""
        if os.path.exists(self.trash_path):
            self._delete_directory(self.trash_path)


    def policy_check(self):
        self._load_from_filelist()

        if self.storage_time:
            for f in self.filelist_dict.keys():
                if (time.time() - os.path.getctime(f)) > self.storage_time * 86400:  # 86400 = sec in day
                    if not os.path.isdir(f):
                        os.remove(f)
                    else:
                         self._delete_directory(f)
                    self.filelist_dict.pop(f)
                    logging.info("Policy by time: deleted " + t)
                    self._save_to_filelist()

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
                logging.info("Policy by size: deleted " + oldest_file)
                if not os.path.isdir(oldest_file):
                    os.remove(oldest_file)
                else:
                     self._delete_directory(oldest_file)

        self._save_to_filelist()

    
    def delete_to_trash_by_reg(self, regular, directory):
        """Removes by regex in directory"""        
        info_message = u""
        exit_code = ExitCodes.GOOD
        del_list = []        
        directory = os.path.abspath(directory)

        if os.path.isdir(directory):
            try:
                self._find_matches(directory, regular, del_list)
            except OSError:
                info_message = u"Unknown message"
                exit_code = ExitCodes.UNKNOWN
        else:
            info_message = u"Not correct path of directory"
            exit_code =  ExitCodes.NO_ACCESS

        if not len(del_list):
            info_message = u"No matches"
            exit_code =  ExitCodes.NO_FILE

        if exit_code == ExitCodes.GOOD:        
            return_list = self.delete_to_trash(del_list)
            self.policy_check()   
            return return_list
        else:
            logging.error(info_message)
            return [(info_message, exit_code)]

    
    def _find_matches(self, directory, regular, lst):
        for f in os.listdir(directory):
            path = os.path.join(directory,f)           
            if re.match(regular, f):
                lst.append(path)                
            else:
                if os.path.isdir(path) and not os.path.islink(path):
                    self._find_matches(path, regular, lst)


def _pickled_delete_to_trash(args):
    trash_obj, target, dct = args
    return trash_obj._delete_to_trash(target, dct)