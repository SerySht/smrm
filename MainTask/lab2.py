import os
import sys
import shutil
import argparse


#I guess all this can be better :)
def clean_trash(trash_location):
	shutil.rmtree(trash_location)
	os.mkdir(trash_location)

def show_trash(trash_location):
	print os.listdir(trash_location) 

def delete_file(filename):
	shutil.remove(filename)

def delete_directory():
	shutil.rmtree(directory_location)

def recover_from_trash(filename):
	f = open('Trash/list.txt', 'r')
	for line in f:
		line = line.split()   #could be better way	
		if filename == line[0]:			
			shutil.move("Trash/"+filename, line[1])
			line = ""   #how delete line, m?
			f.close()
			return
	print "There is no such file!"	
	



def delete_in_trash(filename, file_location, trash_location):
	shutil.move(filename, trash_location)
	f = open('Trash/list.txt', 'a')
	f.write(filename + ' ' + file_location)
	f.close()





def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('type_of_command')
	parser.add_argument('file', nargs='?', default=' ')	
	arguments = parser.parse_args(sys.argv[1:])
	file_location = os.getcwd()
	trash_location = ("Trash/")

	
	if arguments.type_of_command == 'trash':
		delete_in_trash(arguments.file, file_location, trash_location)
	elif arguments.type_of_command == 'recover_from_trash':
		recover_from_trash(arguments.file)
	elif arguments.type_of_command == 'clean_trash':
		clean_trash(trash_location)
	elif arguments.type_of_command == 'show_trash':
		show_trash(trash_location)
	else: print "There is no such command!"

main()