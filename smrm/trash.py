import os
import sys
import json
import shutil
import time
import re
import logging
from utils import confirmed, get_size, conflict_solver, output, Progress


class Trash(object):

    def __init__ (self, trash_path, current_directory = os.getcwd(), storage_time=False, 
                    trash_maximum_size=False, recover_conflict='not_replace', 
                    silent=False, interactive=False, dry_run = False, force = False):

        self.trash_path = trash_path
        self.current_directory = current_directory
        self.storage_time = storage_time
        self.trash_maximum_size = trash_maximum_size
        self.recover_conflict = recover_conflict
        self.silent = silent 
        self.interactive = interactive
        self.dry_run = dry_run 
        self.force = force  
         
        if not os.path.exists(self.trash_path):      
            os.mkdir(self.trash_path) 
        self.filelist_path = os.path.join(self.trash_path, 'filelist')       
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
        
    
    def __mover_to_trash(self, filepath):           
            trash_filepath = os.path.join(self.trash_path, str(os.stat(filepath).st_ino))  
            os.rename(filepath, trash_filepath)
            
            self.__load_from_filelist()           
            self.filelist_dict[trash_filepath] = filepath
            self.__save_to_filelist()   


    def delete_to_trash(self, targets):        
        return_list = []
        exit_code = 0 
        
        for target in targets:
            filepath = os.path.abspath(target)
            if os.path.exists(filepath) or self.force:
                if not self.interactive or confirmed(target):
                    if os.access(filepath, os.W_OK): 
                        if not self.dry_run:
                            self.__mover_to_trash(filepath)
                            return_list.append(target + ' moved to trash ')
                        else:
                            return_list.append('"{0}" will be moved to trash'.format(os.path.basename(filepath)))                
                    else:
                        exit_code = 3
                        logging.error("File not exists or no access to file")
                else:                
                    logging.info("Deleting canceled")
            else:
                exit_code = 3
                logging.error("File not exists")
        
        return return_list, exit_code

        

    def get_which_one(self, recover_list):
        i = 0
        j = 0 
        oldest_file = recover_list[i] 
        for f in recover_list:                 
            if os.path.getctime(f[0]) > os.path.getctime(oldest_file[0]):
                newest_file = f
                j = i  
            i += 1   
        return j 
 
        
    def __mover_from_trash(self, trash_filepath, filepath):
        if os.path.exists(filepath):
            if self.recover_conflict != 'replace':
                while os.path.exists(filepath): 
                    filepath = conflict_solver(filepath)                   
        if not self.dry_run:
                os.rename(trash_filepath, filepath)
                self.filelist_dict.pop(trash_filepath) 
                logging.info("Recovered %s"%filepath)
                return ("Recovered %s"%filepath)
        else:
            return filepath + " will be recovered" 
                    
    

    def recover_from_trash(self, targets):       
        self.__load_from_filelist()
        return_list = []
        exit_code = 0
        
        for target in targets:
            recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == target]            

            if len(recover_list) == 0:
                if not self.silent:
                    return_list.append("There is no such file!!!")
                    exit_code = 1 
                logging.error ("There is no file in trash") 
            
            elif len(recover_list) == 1:
                return_list.append(self.__mover_from_trash(recover_list[0][0], recover_list[0][1]))
            else:
                i = int(self.get_which_one(recover_list))
                return_list.append(self.__mover_from_trash(recover_list[i][0], recover_list[i][1]))
                        
        
        self.__save_to_filelist()        
        return return_list, exit_code
  

    
    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_path)
            os.mkdir(self.trash_path)
            logging.info("Trash wiped")           
        else:
            return ["Trash will be wiped"]

    
    def show_trash(self, n):  
        self.__load_from_filelist()
        return_list = []
        if self.filelist_dict != {}:
            filelist = [item for item in self.filelist_dict.items()[-n:]]
            for i in range(len(filelist)):
                return_list.append('"{0}" deleted from {1} at {2}'.format(os.path.basename(filelist[i][1]), 
                                                                os.path.split(filelist[i][1])[0],
                                                                time.ctime(os.path.getctime(filelist[i][0])))) 
            return return_list
        else:
            logging.info("Trash is empty")
        
    
    
    def policy_check(self):        
        self.__load_from_filelist()
        
        if self.storage_time:
            for f in self.filelist_dict.keys():
                if (time.time() - os.path.getctime(f)) > self.storage_time*86400:  #86400 = sec in day
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
                if not os.path.isdir(oldest_file):
                    os.remove(oldest_file)                        
                else:
                    shutil.rmtree(oldest_file)                
                
        self.__save_to_filelist()


    
    def delete_to_trash_by_reg(self, regular, directory):
        progress = Progress(os.path.abspath(directory))

        for path, directories, files in os.walk(directory):
            for f in files:             
                if re.match(regular, f):
                    if not self.interactive or confirmed(f):
                        progress.inc()                 
                        self.delete_to_trash(os.path.join(path, f))
            if not self.silent:
                progress.show()     

 
    


