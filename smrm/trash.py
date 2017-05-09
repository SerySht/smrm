import os
import json
import shutil
import time
import re
import logging


class Trash(object):

    def __init__ (self, trash_location = os.getenv("HOME"), current_directory = os.getenv("HOME"), storage_time='', trash_maximum_size='', recover_conflict='not_replace', silent=False, i=False, dry_run = False, force = False):

        if storage_time == '':
            self.storage_time = ''
        else: 
            self.storage_time = int(storage_time) *3600

        self.trash_location = trash_location + "/Trash"
        self.current_directory = current_directory
        self.trash_maximum_size = trash_maximum_size
        self.recover_conflict = recover_conflict
        self.silent = silent 
        self.interactive = i
        self.dry_run = dry_run 
        self.force = force  
        self.filelist_location = os.path.join(self.trash_location, 'filelist')      
        
        if not os.path.exists(self.trash_location):      
            os.mkdir(self.trash_location)    
    
    def __load_from_filelist(self): 
        with open(self.filelist_location, 'a+') as filelist:       
            try:
                self.filelist_dict = json.load(filelist)
            except ValueError:
                self.filelist_dict = {}  
      
    def __save_to_filelist(self):
        with open(self.filelist_location, 'w') as filelist:              
            filelist.write(json.dumps(self.filelist_dict))           

    def __confirmed(self, filename):        
        while True:
            answer = raw_input("-Are you sure you want to move \"{0}\" to the Trash?\n".format(filename))
            if answer in {'yes', 'Yes', 'y', 'YES' 'da'}:
                return True
            elif answer in {'No', 'no', 'NO', 'net', 'n'}:
                return False
            else: print "Unknown answer"

    def __get_size(self, filename):
        if not os.path.isdir(filename):
            return os.path.getsize(filename)
        total_size = 0
        for r, d, files in os.walk(filename):
            for f in files:                     
                total_size += os.path.getsize(r+'/'+f)
        return total_size
        
    
    def delete_to_trash(self, filenames):      

        def can_be_deleted(filename):            
            return os.access(filename, os.W_OK) 
                 
        
        def to_trash_mover(filepath):           
            trash_filepath = os.path.join(self.trash_location, str(os.stat(filepath).st_ino)) #may be changed on other way      
            os.rename(filepath, trash_filepath)
            
            self.__load_from_filelist()           
            self.filelist_dict[trash_filepath] = filepath
            self.__save_to_filelist()               


        for filename in filenames:
            filepath = os.path.abspath(filename) 

            if can_be_deleted(filepath) and ((self.interactive and self.__confirmed(filepath)) or not self.interactive):
                if not self.dry_run:
                    to_trash_mover(filepath)
                    
                       
                #if not self.silent or self.dry_run:
                    #print "\"{0}\" successfully moved to trash".format(self.file)                 
    
        #if not self.silent and not self.force:
            #print self.file,"can't be deleted!"
        



    def recover_from_trash(self, filenames):

        def get_which_one(recover_list):
            print "Which one you want to recover?"  
            for i in range(len(recover_list)):
                print recover_list[i][1]
            return int(raw_input()) - 1 

        def conflict_solver(filename):
            try:
                int(filename[filename.rfind('(')+1:filename.rfind(')')])
            except ValueError:
                return filename + '(1)'

            num = int(filename[filename.rfind('(')+1:filename.rfind(')')])
            return filename.replace(str(num), str(num+1))
                     

        def mover_from_trash(trash_filepath, filepath):        

            if not os.path.exists(filepath):
                os.rename(trash_filepath, filepath)             
            else:
                new_filepath = filepath
                if self.recover_conflict != 'replace':
                    while os.path.exists(new_filepath): 
                        new_filepath = conflict_solver(new_filepath)
                
                os.rename(trash_filepath, new_filepath)            
            self.filelist_dict.pop(trash_filepath)            
        

        self.__load_from_filelist()

        for filename in filenames:            
            recover_list = [item for item in self.filelist_dict.items() if os.path.basename(item[1]) == filename ]
            print recover_list

            if recover_list == []:
                print "There is no such file!!!"
                continue

            if len(recover_list) == 1:
                mover_from_trash(recover_list[0][0], recover_list[0][1])
            else:
                i = get_which_one(recover_list)
                mover_from_trash(recover_list[i][0], recover_list[i][1])

            '''
            else:               
                if len(self.lists_by_name) == 1:
                    if not self.dry_run: mover_from_trash(0, filename)  
                    else: print filename, "recovered from the trash"                
                else:                                       
                    if not self.dry_run: 
                        mover_from_trash(get_which_one(), filename)
                    else: 
                        get_which_one()
                        print filename, "recovered from the trash"

                self.dict[filename] = self.lists_by_name
                if len(self.lists_by_name) == 0:                    
                    self.dict.pop(filename)
                '''
                        
                
        self.__save_to_filelist()
        #self.time_politic_check()

    
    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_location)
            os.mkdir(self.trash_location)
        if not self.silent:
            print "Trash wiped!"        


    def show_trash(self):
        self.__load_from_filelist()
        if self.filelist_dict != {}:
            filelist = [item[1] for item in self.filelist_dict.items()]
            for f in filelist:
                print os.path.basename(f), " deleted from ", f


    def time_politic_check(self):        
        if self.storage_time != '':
            self.__load_from_filelist()         
            
            for filename in self.dict:  
                for i in range(len(self.dict[filename])):   
                    lists_by_name = self.dict[filename]
                    if (time.time() - float(lists_by_name[i]['time'])) > self.storage_time:             
                        if not os.path.isdir(self.trash_location + '/' + lists_by_name[i]["key"]):
                            os.remove(self.trash_location + '/' + lists_by_name[i]["key"])
                        else: shutil.rmtree(self.trash_location + '/' + lists_by_name[i]["key"])                    
                        self.dict[filename].pop(i)  
            self.__save_to_filelist()


    def size_politic_check(self, filename):
        if self.trash_maximum_size!= '':            
            size_of_trash = self.__get_size(self.trash_location)        
            if size_of_trash + self.__get_size(filename) > int(self.trash_maximum_size):            
                self.wipe_trash()



    def delete_to_trash_by_reg(self, regular, directory):
        p = Progress(directory)

        for r, d, files in os.walk(directory):
            for f in files:             
                if (re.match(regular, f) and not self.interactive) or (re.match(regular, f) and (self.interactive and self.__confirmed(f))):
                    p.inc()                 
                    self.delete_to_trash([r + '/'+ f])
            if not self.silent:
                p.show()            
        self.time_politic_check()
    
  


class Progress(object):
    def __init__ (self, filename):
        self.num = 0
        self.all_ = sum([len(files) + len(d) for r, d, files in os.walk(filename)])
        self.proc = 0

    def inc(self):
        self.num += 1   

    def show(self):
        if self.proc != int((float(self.num) / self.all_) * 100):
            self.proc = int((float(self.num) / self.all_) * 100)
            print str(self.proc) + '%'