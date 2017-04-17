import os
import json
import shutil
import deleter



def recover_from_trash(filenames, trash_location):
	f = open(trash_location + '/' + "filelist", 'a+')               
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

	for i in range(len(files)):
		if files[i] not in not_for_delete_set:			
			key = os.stat(files[i]).st_ino
			os.rename(files[i], str(key))
			shutil.move(str(key), trash_location)
			if d.get(files[i]) == None:
				d[files[i]] = [[location, key]]
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
	for i in d:
		print i, ' deleted from: ', d[i]
	f.close()