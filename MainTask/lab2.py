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

def recover_trash():
	pass

def delete_in_trash(filename, file_location, trash_location):
	shutil.move(filename, trash_location)
	f = open('Trash/list.txt', 'a')
	f.write(file_location+filename)
	f.close()






def main():
	#parser = argparse.ArgumentParser()
	#parser.add_argument('--file', default = "filetest")
	#parser.add_argument('--trash_location', default = 'testtrash')
	#parser.add_argument('command')

	#arguments = parser.parse_args(sys.argv[1:]) 
	#print arguments.file
	#print arguments.trash_location
	#if arguments.command = 'cleantrash':

	

main()