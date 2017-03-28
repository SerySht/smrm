import os
import sys
import shutil
import argparse
import ConfigParser


#I guess all this can be better :)
def clean_trash(trash_location):
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
	parser.add_argument('type_of_command')
	parser.add_argument('file', nargs='?', default=' ')	
	arguments = parser.parse_args(sys.argv[1:])
	file_location = os.getcwd()
	trash_location = ("Trash/")
	conf = ConfigParser.RawConfigParser()
	conf.read("smart_rm.conf")
	print conf.get("main", "trash_location")

	
	if arguments.type_of_command == 'trash':
		delete_to_trash(arguments.file, file_location, trash_location)

	elif arguments.type_of_command == 'recover_from_trash':
		recover_from_trash(arguments.file)
	elif arguments.type_of_command == 'clean_trash':
		clean_trash(trash_location)
	elif arguments.type_of_command == 'show_trash':
		show_trash(trash_location)
	elif arguments.type_of_command == 'without_recover':
		delete_file(arguments.file)
	else: print "There is no such command!"

main()