import os
import json
import shutil
import deleter
import time



def trash_dry_run(f):
	def wrapped():
		pass
	return wrapped


def load_from_filelist(trash_location):
	f = open(trash_location + '/' + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		d = {}  
	f.close() 
	return d


def load_to_filelist(trash_location, d):
	f = open(trash_location +'/' + "filelist", 'w')  
	f.write(json.dumps(d))
	f.close()


def delete_to_trash(filenames, location, trash_location, silent):
	d = load_from_filelist(trash_location) 	
	not_for_delete_set = set()
	not_for_delete_set.add(trash_location)	

	for filename in filenames: 
		if filename not in not_for_delete_set:			
			key = str(os.stat(filename).st_ino)  #id
			os.rename(filename, key)
			shutil.move(key, trash_location)
			
			if d.get(filename) == None:
				d[filename] = [{'location':location, 'key':key, 'time':str(time.time())}]
			else:
				d[filename].append({'location':location, 'key':key, 'time':str(time.time())})
		else:
			print d[filename]," can't be deleted!"
	
	load_to_filelist(trash_location, d)
	
	if not silent:
		print "Successfully moved to trash!"



def recover_from_trash(filenames, trash_location):
	d = load_from_filelist(trash_location)

	for filename in filenames:
		list_of_files = d.get(filename)		
		
		if list_of_files == None:
			print "There is no such file!!!"
			continue	
		
		else:
			if len(list_of_files) == 1:				
				shutil.move(trash_location + '/' + list_of_files[0]["key"], list_of_files[0]["location"]) 
				os.rename(list_of_files[0]["key"], filename)
				d.pop(filename) 
			else:
				print "Which one you want to recover?"	
				for i in range(len(list_of_files)):
					print "#{0} from {1}".format(i+1, list_of_files[i]["location"])
				number = int(raw_input()) - 1
				
				shutil.move(trash_location + '/' + list_of_files[number]["key"], list_of_files[number]["location"])
				os.rename(str(list_of_files[number]['key']), filename)
				list_of_files.pop(number)
				d[filename] = list_of_files

	load_to_filelist(trash_location, d)



def wipe_trash(trash_location):
	deleter.recursive_delete(trash_location)
	os.mkdir(trash_location)



def show_trash(trash_location):
	d = load_from_filelist(trash_location)
	if d != {}:
		for filename in d:		
			for f in d[filename]:
				print "{0} deleted from {1}".format(str(filename), f["location"])					
	else:	
		print "Trash is empty!"



def check_trash(trash_location, storage_time):
	d = load_from_filelist(trash_location)	
	t = time.time()
	
	for filename in d:	
		i = -1	
		for f in d[filename]:
			i += 1
			if (t - float(f['time'])) > int(storage_time):
				print "lol kek cheburek ", f
				os.remove(trash_location + '/' + f["key"])
				d[filename].pop(i) 	
				#if len(d[filename]) == 0:
					#d.pop(filename)
			else:
				print (t - float(f['time']))				
	
	load_to_filelist(trash_location, d)
