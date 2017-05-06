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
        
        if not os.path.exists(self.trash_location):      
            os.mkdir(self.trash_location)    
    
    def __load_from_filelist(self): 
        f = open(self.trash_location + "/filelist", 'a+')               
        try:
            self.dict = json.load(f)
        except ValueError:
            self.dict = {}  
        f.close()       

    def __save_to_filelist(self):
        f = open(self.trash_location + "/filelist", 'w')  
        f.write(json.dumps(self.dict))
        f.close()       

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

        def location_parser(current_directory, filename):
            i = filename.rfind('/') 
            if i == -1: 
                return current_directory + '/', filename
            else:
                location, filename = filename[:i+1], filename[i+1:]             
                if len(location)>0 and location[0] == '/':
                    return location,  filename
                else: return current_directory + '/' + location, filename


        def can_be_deleted(filename): 
            return os.access(filename, os.W_OK) and filename.find('/home') == 0
            pass
    
        
        def to_trash_mover(filename):
            self.size_politic_check(filename)
            self.key = str(os.stat(filename).st_ino)            
            os.rename(filename, self.trash_location + '/' + self.key)

        def add_to_filelist():
            self.__load_from_filelist()     
            if self.dict.get(self.file) == None:
                self.dict[self.file] = [{'location':self.file_location, 
                                            'key':self.key, 
                                            'time':str(time.time()), 
                                            'size':self.__get_size(self.trash_location+ '/' + self.key)}]
            else:
                self.dict[self.file].append({'location':self.file_location, 
                                            'key':self.key, 'time':str(time.time()),
                                            'time':str(time.time()),
                                            'size':self.__get_size(self.trash_location+'/'+ self.key)})
            self.__save_to_filelist()   

        for filename in filenames:
            self.sfile_location, self.file = location_parser(self.current_directory, filename)

            if can_be_deleted(self.file_location + self.file) and ((self.interactive and self.__confirmed(self.file)) or not self.interactive):
                if not self.dry_run:
                    to_trash_mover(filename)
                    add_to_filelist()
                    
                if not self.silent or self.dry_run:
                    print "\"{0}\" successfully moved to trash".format(self.file)   
            elif not self.silent and not self.force:
                print self.file,"can't be deleted!"
        self.time_politic_check()


    def recover_from_trash(self, filenames):

        def get_which_one():
            print "Which one you want to recover?"  
            for i in range(len(self.lists_by_name)):
                print "#{0} from {1} deleted at {2}".format(i+1, self.lists_by_name[i]["location"], time.ctime(float(self.lists_by_name[i]["time"])))
            return int(raw_input()) - 1 

        def conflict_solver(filename):
            try:
                int(filename[filename.rfind('(')+1:filename.rfind(')')])
            except ValueError:
                return filename + '(1)'

            num = int(filename[filename.rfind('(')+1:filename.rfind(')')])
            return filename.replace(str(num), str(num+1))
                     

        def mover_from_trash(i, filename):  
            if not os.path.exists(self.lists_by_name[i]["location"] + '/' + filename):
                os.rename(self.trash_location + '/' + self.lists_by_name[i]['key'], self.lists_by_name[i]["location"] + '/' + filename)             
            else:
                new_filename = self.lists_by_name[i]["location"] + '/' + filename
                if self.recover_conflict != 'replace':
                    while os.path.exists(new_filename): 
                        new_filename = conflict_solver(new_filename)
                
                os.rename(self.trash_location + '/' + self.lists_by_name[i]['key'], new_filename)
            
            self.lists_by_name.pop(i)   
        

        self.__load_from_filelist()

        for filename in filenames:
            self.lists_by_name = self.dict.get(filename)                
            if self.lists_by_name == None:
                print "There is no such file!!!"
                continue    
            
            else:               
                if len(self.lists_by_name) == 1:
                    if not self.dry_run: mover_from_trash(0, filename)  
                    else: print filename, "recovered from the trash"                
                else:                                       
                    if not self.dry_run: mover_from_trash(get_which_one(), filename)
                    else: 
                        get_which_one()
                        print filename, "recovered from the trash"

                self.dict[filename] = self.lists_by_name
                if len(self.lists_by_name) == 0:                    
                    self.dict.pop(filename)
                
                        
                
        self.__save_to_filelist()
        self.time_politic_check()


    def wipe_trash(self):
        if not self.dry_run:
            shutil.rmtree(self.trash_location)
            os.mkdir(self.trash_location)
        if not self.silent:
            print "Trash wiped!"        


    def show_trash(self):
        self.__load_from_filelist()
        if self.dict != {}:
            for filename in self.dict:      
                for f in self.dict[filename]:
                    print "\"{0}\" was deleted from: {1} at {2}".format(str(filename), f["location"], time.ctime(float(f["time"])))                 
                
        elif not self.silent:   
            print "Trash is empty!"
        self.time_politic_check()


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