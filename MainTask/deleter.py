import os
import re
import logging

logging.basicConfig(filename='smart_rm.log',level=logging.DEBUG)

def delete(list_of_files, interactive = False):
	for i in range(len(list_of_files)): 
			if os.path.isdir(list_of_files[i]):
				print "It is directory"
			else:
				if not interactive:
					os.remove(list_of_files[i])
				else:
					if confirmed:
						os.remove(list_of_files[i])


def delete_by_reg(regular, directory):
	files = os.listdir(directory)
	regular = '\\' + regular
	logging.debug(regular)
	for i in range(len(files)):
		if re.match(regular, files[i]):
			os.remove(directory + '/' + files[i])


def recursive_delete(directory, interactive = False):
	if len(os.listdir(directory)) == 0:
		if not interactive:	
			os.rmdir(directory) 
		else:
			if confirmed(directory):
				os.rmdir(directory)	
	else:
		stack = [directory]
		files = os.listdir(directory)
		for i in range(len(files)):
			stack.append(directory + '/' + files[i])    #adding files in stack
		while len(stack)>0:
			f = stack.pop()
			logging.debug(regular)
			if os.path.isdir(f):  
				recursive_delete(f, interactive)
			else: 
				if not interactive:
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

	 	