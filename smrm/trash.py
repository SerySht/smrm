import os
import sys
import json
import shutil
import time
import re
import logging
from utils import confirmed, get_size, conflict_solver, Progress


class Trash(object):

    def __init__ (self, trash_path, current_directory = os.getcwd(), storage_time=False, 
                    trash_maximum_size=False, recover_conflict='not_replace', 
                    silent=False, interactive=False, dry_run = False, force = False):

        if storage_time != '':             
            self.storage_time = int(storage_time) 

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
        self.filelist_location = os.path.join(self.trash_path, 'filelist')        
        
        logging.info("Trash path {}".format(trash_path)) 
    
    
    def load_from_filelist(self): 
        with open(self.filelist_location, 'a+') as filelist:       
            try:
                self.filelist_dict = json.load(filelist)
            except ValueError:
                self.filelist_dict = {}  
      
    
    def save_to_filelist(self):
        with open(self.filelist_location, 'w+') as filelist:              
            filelist.write(json.dumps(self.filelist_dict))            
        
    
    def mover_to_trash(self, filepath):           
            trash_filepath = os.path.join(self.trash_path, str(os.stat(filepath).st_ino))  
            os.rename(filepath, trash_filepath)
            
            self.load_from_filelist()           
            self.filelist_dict[trash_filepath] = filepath
            self.save_to_filelist()   


    def delete_to_trash(self, target):
        filepath = os.path.abspath(target)
        if os.path.exists(filepath) or self.force:
            if not self.interactive or confirmed(target):
                if os.access(filepath, os.W_OK): 
                    if not self.dry_run:
                        self.mover_to_trash(filepath)
                    else:
                        print '"{0}" will be moved to trash'.format(os.path.basename(filepath))                
                else:
                    logging.error("File not exists or no access to file")
            else:
                logging.info("Deleting canceled")
        else:
            logging.error("File not exists")
                
        

    def get_which_one(self, recover_list):
        print "Which one you want to recover?"  
        for i in range(len(recover_list)):
            print '#{0} "{1}" deleted from {2} at {3}'.format(i+1, os.path.basename(recover_list[i][1]), 
                                                                os.path.split(recover_list[i][1])[0],
                                                                time.ctime(os.path.getctime(recover_list[i][0])))  
        
        return int(raw_input()) - 1   #add check
        

    def mover_from_trash(self, trash_filepath, filepath):
        if os.path.exists(filepath):
            if self.recover_conflict != 'replace':
                while os.path.exists(filepath): 
                    filepath = conflict_solver(filepath)
                     
        if not self.dry_run:
                os.rename(trash_filepath, filepath)
                self.filelist_dict.pop(trash_filepath) 
                logging.info("Recovered %s"%filepath)
        else:
            print filepath, "will be recovered" 
                    
    

    def recover_from_trash(self, target):       
        self.load_from_filelist()

        recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == target]            

        if len(recover_list) == 0:
            if not self.silent:
                print "There is no such file!!!" 
            logging.error ("There is no file in trash") 
        
        elif len(recover_list) == 1:
            self.mover_from_trash(recover_list[0][0], recover_list[0][1])
        else:
            i = int(self.get_which_one(recover_list))
            self.mover_from_trash(recover_list[i][0], recover_list[i][1])
                    
        self.save_to_filelist()
  

    
    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_path)
            os.mkdir(self.trash_path)
            logging.info("Trash wiped")               
        else:
            print "Trash will be wiped"

    
    def show_trash(self, n):  
        self.load_from_filelist()
        if self.filelist_dict != {}:
            filelist = [item for item in self.filelist_dict.items()[-n:]]
            for i in range(len(filelist)):
                print '"{0}" deleted from {1} at {2}'.format(os.path.basename(filelist[i][1]), 
                                                                os.path.split(filelist[i][1])[0],
                                                                time.ctime(os.path.getctime(filelist[i][0])))  
        else:
            logging.info("Trash is empty")
        
    
    
    def policy_check(self):        
        self.load_from_filelist()
        
        if self.storage_time:
            for f in self.filelist_dict.keys():
                if (time.time() - os.path.getctime(f)) > self.storage_time*86400:  #86400 = sec in day
                    if not os.path.isdir(f):
                        os.remove(f)                        
                    else:
                        shutil.rmtree(f)                        
                    self.filelist_dict.pop(f)
                    self.save_to_filelist()
        
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
                
        self.save_to_filelist()


    
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

 
    


