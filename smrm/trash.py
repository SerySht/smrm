import os
import json
import shutil
import time
import re
import logging
from utils import confirmed, get_size, conflict_solver, Progress


class Trash(object):

    def __init__ (self, trash_path, current_directory = os.getcwd(), storage_time='', trash_maximum_size='', recover_conflict='not_replace', silent=False, i=False, dry_run = False, force = False):

        if storage_time == '':
            self.storage_time = ''
        else: 
            self.storage_time = int(storage_time) 

        self.trash_path = trash_path
        self.current_directory = current_directory
        self.trash_maximum_size = trash_maximum_size
        self.recover_conflict = recover_conflict
        self.silent = silent 
        self.interactive = i
        self.dry_run = dry_run 
        self.force = force  
        
        if not os.path.exists(self.trash_path):      
            os.mkdir(self.trash_path) 
        self.filelist_location = os.path.join(self.trash_path, 'filelist')        
    
    
    def load_from_filelist(self): 
        with open(self.filelist_location, 'a+') as filelist:       
            try:
                self.filelist_dict = json.load(filelist)
            except ValueError:
                self.filelist_dict = {}  
      
    
    def save_to_filelist(self):
        with open(self.filelist_location, 'w') as filelist:              
            filelist.write(json.dumps(self.filelist_dict))            
        
    
    def mover_to_trash(self, filepath):           
            trash_filepath = os.path.join(self.trash_path, str(os.stat(filepath).st_ino))      
            os.rename(filepath, trash_filepath)
            
            self.load_from_filelist()           
            self.filelist_dict[trash_filepath] = filepath
            self.save_to_filelist()   


    def delete_to_trash(self, target):
        filepath = os.path.abspath(target)

        if os.access(filepath, os.W_OK) and ((self.interactive and confirmed(filepath)) or not self.interactive):
            if not self.dry_run:
                self.mover_to_trash(filepath)
                
            #if not self.silent or self.dry_run:
                #print "\"{0}\" moved to trash".format(os.path.basename(filepath))                

        elif not self.silent and not self.force:  #add why
            print os.path.basename(filepath),"can't be deleted!"
        

    def get_which_one(self, recover_list):
        print "Which one you want to recover?"  
        for i in range(len(recover_list)):
            print "#{0} \"{1}\" deleted from {2} at {3}".format(i+1, os.path.basename(recover_list[i][1]), 
                                                                os.path.split(recover_list[i][1])[0],
                                                                    os.path.getctime(recover_list[i][0]))   #fix time
        return int(raw_input()) - 1    

    
    def mover_from_trash(self, trash_filepath, filepath):        

        if not os.path.exists(filepath):
            os.rename(trash_filepath, filepath)             
        else:
            new_filepath = filepath
            if self.recover_conflict != 'replace':
                while os.path.exists(new_filepath): 
                    new_filepath = conflict_solver(new_filepath)
            
            os.rename(trash_filepath, new_filepath)            
        self.filelist_dict.pop(trash_filepath)            
    

    def recover_from_trash(self, target):       
        self.load_from_filelist()

        recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == target]            

        if len(recover_list) == 0:
            print "There is no such file!!!"  
        elif len(recover_list) == 1:
            self.mover_from_trash(recover_list[0][0], recover_list[0][1])
        else:
            i = self.get_which_one(recover_list)
            self.mover_from_trash(recover_list[i][0], recover_list[i][1])
                    
        self.save_to_filelist()
       

    
    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_path)
            os.mkdir(self.trash_path)
        if not self.silent:
            logging.info("Trash wiped")
            print "Trash wiped!"        


    def show_trash(self):
        self.load_from_filelist()
        if self.filelist_dict != {}:
            filelist = [item for item in self.filelist_dict.items()]
            for i in range(len(filelist)):
                print "\"{0}\" deleted from {1} at {2}".format(os.path.basename(filelist[i][1]), 
                                                                os.path.split(filelist[i][1])[0],
                                                                    os.path.getctime(filelist[i][0]))   #fix time


    def time_politic_check(self):        
        if self.storage_time != '':
            self.load_from_filelist()         
            
            for filename in self.dict:  
                for i in range(len(self.dict[filename])):   
                    lists_by_name = self.dict[filename]
                    if (time.time() - float(lists_by_name[i]['time'])) > self.storage_time:             
                        if not os.path.isdir(self.trash_path + '/' + lists_by_name[i]["key"]):
                            os.remove(self.trash_path + '/' + lists_by_name[i]["key"])
                        else: shutil.rmtree(self.trash_path + '/' + lists_by_name[i]["key"])                    
                        self.dict[filename].pop(i)  
            self.save_to_filelist()


    def size_politic_check(self, filename):
        if self.trash_maximum_size!= '':            
            size_of_trash = self.__get_size(self.trash_path)        
            if size_of_trash + self.__get_size(filename) > int(self.trash_maximum_size):            
                self.wipe_trash()



    def delete_to_trash_by_reg(self, regular, directory):
        p = Progress(os.path.abspath(directory))

        for r, d, files in os.walk(directory):
            for f in files:             
                if (re.match(regular, f) and not self.interactive) or (re.match(regular, f) and (self.interactive and self.__confirmed(f))):
                    p.inc()                 
                    self.delete_to_trash(os.path.join(r,f))
            if not self.silent:
                p.show()            
        
    
  

