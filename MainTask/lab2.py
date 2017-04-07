import os
import re
import sys
import json
import shutil
import argparse
import ConfigParser


def wipe_trash(trash_location):
	recursive_delete(trash_location)
	os.mkdir(trash_location)


def show_trash(trash_location):
	print os.listdir(trash_location) 

def delete(list_of_files, confirm = False):
	for i in range(len(list_of_files)): 
			if os.path.isdir(list_of_files[i]):
				print "It is directory"
			else:
				if confirm and confirmed(list_of_files[i]):
					os.remove(list_of_files[i])
				else:
					if not confirm:
						os.remove(list_of_files[i])


def recover_from_trash(filenames, trash_location):
	f = open(trash_location + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		d = {}  
	f.close() 

	for filename in filenames:
		try: file_location = d.pop(filename)		
		except KeyError:
			print "There is no such file!!!"
			continue		
		shutil.move(trash_location + '/' + filename, file_location)

	f = open(trash_location + "filelist", 'w')    #may be better way
	f.write(json.dumps(d))
	f.close()


def delete_to_trash(files, location, trash_location):
	f = open(trash_location + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		d = {}  
	f.close()  	
	for i in range(len(files)):
		shutil.move(files[i], trash_location)
		d[files[i]] = location	
	f = open(trash_location + "filelist", 'w')    #may be better way
	f.write(json.dumps(d))
	f.close()


def delete_by_reg(directory, regular):
	files = os.listdir(directory)
	for i in range(len(files)):
		if re.match(regular, files[i]):
			os.remove(files[i])


def recursive_delete(directory, confirm = False):
	if len(os.listdir(directory)) == 0:
		os.rmdir(directory) 
	else:
		stack = [directory]
		files = os.listdir(directory)
		for i in range(len(files)):
			stack.append(directory + '/' + files[i])    #adding files in stack
		while len(stack)>0:
			f = stack.pop()
			print f
			if os.path.isdir(f):
				recursive_delete(f)
			else: 
				if not confirm:
					os.remove(f)
				else:
					if confirmed(directory):
						os.remove(f)


def confirmed(filename):
	answer = raw_input("-Are you sure that you want delete {0}?\n".format(filename))
	if answer in {'yes', 'Yes', 'y', 'YES' 'da'}:
		return True
	elif answer in {'No', 'no', 'NO', 'net'}:
		return False
	else: print "Unknown answer"

	 	



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('files', nargs='*', default='')	
	parser.add_argument('-t', nargs='*', default='')   
	parser.add_argument('-st', nargs='?', default='')
	parser.add_argument('-wt', nargs='?', default='')
	parser.add_argument('-recover', nargs='*', default='')
	parser.add_argument('-i', nargs='*', default='')
	parser.add_argument('-r', nargs='?', default='')
	parser.add_argument('-reg', nargs='?', default='')
	arguments = parser.parse_args(sys.argv[1:])
	print arguments

	location = os.getcwd()  ####fixxxxxxxxxxxxx	
	
	conf = ConfigParser.RawConfigParser()            #<<-----config
	conf.read("smart_rm.conf")
	trash_location = conf.get("main", "trash_location")
	

	if arguments.files != '':
		delete(arguments.files)
	
	elif arguments.t != '':       
		delete_to_trash(arguments.t, location, trash_location)

	elif arguments.st != '':
		show_trash(trash_location)

	elif arguments.wt != '':
		wipe_trash(trash_location)

	elif arguments.recover != '':
		recover_from_trash(arguments.recover, trash_location)

	elif arguments.i != '':
		delete(arguments.i, confirm = True) 
	elif arguments.reg != '':
		delete_by_reg(arguments.reg)
	elif arguments.r != '':
		recursive_delete(arguments.r)		
	else:
		delete_file(arguments.file)
main()
