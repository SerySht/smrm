import os
import re
import logging


def delete(filenames, interactive = False):
	for filename in filenames: 
			if os.path.isdir(filename):
				print "Can't be deleted: it is directory! \nUse parameter -r to delete directory."
			else:				
				if (not interactive) or (interactive and confirmed(filename)):
					try:
						os.remove(filename)
					except:
						print "There is no such file!"
				

def recursive_delete(directory, interactive = False):
	if len(os.listdir(directory)) == 0:
		if (not interactive) or (interactive and confirmed(filename)):
			os.rmdir(directory) 	
	else:
		stack = [directory]
		files = os.listdir(directory)
		for f in files:
			stack.append(directory + '/' + f)    #adding files in stack
		
		while len(stack)>0:
			f = stack.pop()			
			if os.path.isdir(f):  
				recursive_delete(f, interactive)
			else: 
				if not interactive:
					os.remove(f)
				else:
					if confirmed(f):
						os.remove(f)
					else:
						print "The directory can't be deleted until it be empty!"
						return 

def confirmed(filename):
	answer = raw_input("-Are you sure that you want delete {0}?\n".format(filename))
	if answer in {'yes', 'Yes', 'y', 'YES' 'da'}:
		return True
	elif answer in {'No', 'no', 'NO', 'net', 'n'}:
		return False
	else: print "Unknown answer"


def delete_by_reg(regular, directory):
	#recursive
	#to trash
	#-i
	files = os.listdir(directory)
	regular = '\\' + regular
	
	for i in range(len(files)):
		if re.match(regular, files[i]):
			os.remove(directory + '/' + files[i])
	 	