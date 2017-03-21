import os
import sys
import shutil
import argparse


#I guess it can be better :)
def clean_trash(trash_location):
	shutil.rmtree(trash_location)
	os.mkdir(trash_location)

def watch_trash(trash_location):
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
	f.close()
	#add deleting from list



def delete_in_trash(filename, file_location, trash_location):
	shutil.move(filename, trash_location)
	f = open('Trash/list.txt', 'a')
	f.write(filename + ' ' + file_location)
	f.close()





def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('type_of_command')
	parser.add_argument('file')	
	file_location = os.getcwd()
	trash_location = ("Trash")

	arguments = parser.parse_args(sys.argv[1:]) 
	if arguments.type_of_command == 'trash':
		delete_in_trash(arguments.file, file_location, trash_location)
	elif arguments.type_of_command == 'recover_from_trash':
		recover_from_trash(arguments.file)
	

main()