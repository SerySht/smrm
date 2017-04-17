import os
import json
import shutil
import deleter
from datetime import datetime

def trash_dry_run(f):
	def wrapped():
		pass
	return wrapped


def recover_from_trash(filenames, trash_location):
	f = open(trash_location + '/' + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		d = {}  
	f.close() 

	for filename in filenames:
		files = d.get(filename)		
		if files == None:
			print "There is no such file!!!"
			continue	
		else:
			if len(files)==1:				
				shutil.move(trash_location + '/' + str(files[0][1]), files[0][0])
				os.rename(str(files[0][1]), filename)
				d.pop(filename) 
			else:
				print "Which one you want to recover?"	
				for i in range(len(files)):
					print "#{0} from {1}".format(i+1, files[i][0])
				number = int(raw_input()) - 1
				shutil.move(trash_location + '/' + str(files[number][1]), files[number][0])
				os.rename(str(files[number][1]), filename) #add location
				files.pop(number)
				d[filename] = files




	f = open(trash_location +'/' + "filelist", 'w')    #may be better way
	f.write(json.dumps(d))
	f.close()


def delete_to_trash(files, location, trash_location):
	not_for_delete_set = set()
	not_for_delete_set.add(trash_location)

	f = open(trash_location + '/' + "filelist", 'a+')
	try:
		d = json.load(f)
	except:					#find Error for json
		d = {}  
	f.close() 

	for i in range(len(files)):  # fix^
		if files[i] not in not_for_delete_set:			
			key = os.stat(files[i]).st_ino
			os.rename(files[i], str(key))
			shutil.move(str(key), trash_location)
			if d.get(files[i]) == None:
				d[files[i]] = [[location, key, str(datetime.now())]]
			else:
				l = []
				l.extend(d.get(files[i]))
				l.append([location, key])
				d[files[i]]	= l
		else:
			print "Chto mertvo umeret ne moget"
	
	f = open(trash_location + '/' + "filelist", 'w')    #may be better way
	f.write(json.dumps(d))
	f.close()



def wipe_trash(trash_location):
	deleter.recursive_delete(trash_location)
	os.mkdir(trash_location)


def show_trash(trash_location):
	#problemi (too big trash)
	f = open(trash_location +'/' + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		print "Trash is empty!"
		return
	for files in d:		
		for i in range(len(d.get(files))):
			print files, ' deleted from: ', d.get(files)[i][0]
	f.close()