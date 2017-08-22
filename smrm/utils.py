# coding: utf8
import os
import sys


def confirmed(filename):        
    answer = raw_input("-Are you sure you want to move \"{0}\" to the Trash?\n".format(filename))
    if answer in {'yes', 'Yes', 'y', 'YES' 'da'}:
        return True
    elif answer in {'No', 'no', 'NO', 'net', 'n'}:
        return False
    else: confirmed(filename)


def get_size(filepath):
    if not os.path.isdir(filepath):
        return os.path.getsize(filepath)
    total_size = 0
    for r, d, files in os.walk(filepath):
        for f in files:                     
            total_size += os.path.getsize(os.path.join(r, f))
    return total_size


def conflict_solver(filepath):
    try:
        num = int(filepath[filepath.rfind('(')+1:filepath.rfind(')')])
    except ValueError:
        return filepath + '(1)'   
    return filepath.replace('('+str(num)+')', '('+str(num+1)+')')


def output(output_data, silent):    
    exit_code = ExitCodes.GOOD
    for dat in output_data:       
        if dat[1] != ExitCodes.GOOD:
            exit_code = dat[1]
            if not silent:
                if exit_code == ExitCodes.CONFLICT:
                    print "Name confilct solved: ", dat[0]
                else:
                    print "Error smrm: ", dat[0] 
        else:
            if not silent and dat[0] != '':
                print dat[0]
    sys.exit(exit_code)


def get_list_of_directories(directory):
    dir_list = []
    for path, directories, files in os.walk(directory):
        for d in directories:           
            dir_list.append(os.path.join(path, d))
    return dir_list


class ExitCodes(object):  

    GOOD = 0

    CONFLICT = 1

    UNKNOWN = 2

    NO_FILE = 3


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

    def end(self):
        print "100%"        


#os.path.dirname(__file__)