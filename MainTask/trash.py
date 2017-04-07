import os
import json
import shutil
import deleter



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



def wipe_trash(trash_location):
	recursive_delete(trash_location)
	os.mkdir(trash_location)


def show_trash(trash_location):
	print os.listdir(trash_location)