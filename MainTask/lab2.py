import os
import sys
import shutil
import argparse
import ConfigParser


#I guess all this can be better :)
def wipe_trash(trash_location):
	shutil.rmtree(trash_location)
	os.mkdir(trash_location)

def show_trash(trash_location):
	print os.listdir(trash_location) 

def delete_file(filename):
	os.remove(filename)

def delete_directory():
	shutil.rmtree(directory_location)

def recover_from_trash(filename):
	file_list = []
	f = open('Trash/list.txt', 'r+')
	for line in f:
		file_list.append(line)
	if file_list[0] == '\n':
		file_list.pop(0)   #deleting first \n
	f.close()
	


	for i in xrange(len(file_list)):
		line = file_list[i].split()   #could be better way	
		if filename == line[0]:			
			shutil.move("Trash/"+filename, line[1])
			file_list.pop(i)			
			f = open('Trash/list.txt', 'w')
			f.writelines(file_list)
			f.close()
			return
	print "There is no such file!"	
	



def delete_to_trash(filename, file_location, trash_location):
	shutil.move(filename, trash_location)
	f = open('Trash/list.txt', 'a')
	f.write('\n' + filename + ' ' + file_location)
	f.close()





def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', nargs='?', default='')	
	parser.add_argument('-t', nargs='?', default='')
	parser.add_argument('-st', nargs='?', default='')
	parser.add_argument('-wt', nargs='?', default='')
	parser.add_argument('-r', nargs='?', default=''))
	arguments = parser.parse_args(sys.argv[1:])
	
	file_location = os.getcwd()  ####fixxxxxxxxxxxxx
	
	conf = ConfigParser.RawConfigParser()            #<<-----config
	conf.read("smart_rm.conf")
	trash_location = conf.get("main", "trash_location")

	
	if arguments.t != '':
		delete_to_trash(arguments.t, file_location, trash_location)
	elif arguments.st != '':
		show_trash(trash_location)
	elif arguments.wt != '':
		wipe_trash(trash_location)
	elif arguments.r != '':
		recover_from_trash(arguments.r)
	else:
		delete_file(arguments.file)
main()