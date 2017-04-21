import os
import json
import shutil
import deleter
import time
import re
import logging



def load_from_filelist(trash_location):	
	f = open(trash_location + '/' + "filelist", 'a+')               
	try:
		d = json.load(f)
	except ValueError:
		d = {}  
	f.close() 
	return d


def save_to_filelist(trash_location, d):
	f = open(trash_location +'/' + "filelist", 'w')  
	f.write(json.dumps(d))
	f.close()


def add_slash(p):
	if p[0] != '/':
		return '/' + p
	return p


def get_name(filename):
	i = filename.rfind('/')	
	if i > 0: 
		return add_slash(filename[0:i+1]), filename[i+1:]
	return '', filename


def can_be_deleted(filename):
	return os.access(filename, os.W_OK)


def location_check(location, location_add):
	if location_add.find(location) == 0:
		return location_add
	return location + '/'+ location_add


def delete_to_trash(filenames, location, trash_location, silent=False):
	logging.info("In delete_to_trash")
	
	d = load_from_filelist(trash_location) 	

	for filename in filenames:
		location_add, f = get_name(filename)				
		if can_be_deleted(filename):	
			logging.debug(f)		 	
			key = str(os.stat(filename).st_ino)  #id
			os.rename(filename, key)			
			shutil.move(key, trash_location)	
			if not silent:
				print "\"{0}\" successfully moved to trash".format(f)		
			if d.get(f) == None:
				d[f] = [{'location':location_check(location, location_add), 'key':key, 'time':str(time.time()), 'size':os.path.getsize(trash_location+'/' + key)}]
			else:
				d[f].append({'location':location_check(location, location_add), 'key':key, 'time':str(time.time()),'size':os.path.getsize(trash_location+'/'+key)})
		else:
			print f," can't be deleted!"
	
	save_to_filelist(trash_location, d)
	
	



def recover_from_trash(filenames, trash_location, recover_conflict):
	logging.info("In recover_from_trash")

	d = load_from_filelist(trash_location)

	for filename in filenames:
		list_of_files = d.get(filename)				
		if list_of_files == None:
			print "There is no such file!!!"
			continue	
		
		else:
			if len(list_of_files) == 1:				
				os.rename(trash_location + '/' + list_of_files[0]['key'], list_of_files[0]["location"] + '/' + filename)
				d.pop(filename) 
			else:
				print "Which one you want to recover?"	
				for i in range(len(list_of_files)):
					print "#{0} from {1}".format(i+1, list_of_files[i]["location"])
				number = int(raw_input()) - 1
				os.rename(trash_location + '/' + list_of_files[number]['key'], list_of_files[number]["location"] + '/' + filename)
				list_of_files.pop(number)
				d[filename] = list_of_files				

	save_to_filelist(trash_location, d)



def wipe_trash(trash_location):
	deleter.recursive_delete(trash_location)
	os.mkdir(trash_location)



def show_trash(trash_location):
	d = load_from_filelist(trash_location)
	if d != {}:
		for filename in d:		
			for f in d[filename]:
				print "\"{0}\" was deleted from: {1}".format(str(filename), f["location"])					
	else:	
		print "Trash is empty!"



def check_trash(trash_location, storage_time, trash_maximum_size):
	logging.info("In check_trash")

	d = load_from_filelist(trash_location)	
	t = time.time()
	c = d.copy()
	for filename in d:	
		i = -1	
		for f in d[filename]:
			i += 1
			if (t - float(f['time'])) > int(storage_time):				
				os.remove(trash_location + '/' + f["key"])
				c[filename].pop(i) 	
				if len(c[filename]) == 0:
					c.pop(filename)
			else:
				logging.info("\"{0}\" will be deleted in {1} sec".format(filename, int(t - float(f['time']))))	
	d = c
	save_to_filelist(trash_location, d)




def delete_to_trash_by_reg(regular, directory, location, trash_location, interactive = False):		
	files = os.listdir(directory)
	for f in files:		
		if not os.path.isdir(directory + '/' + f): 			
			if (re.match(regular, f) and not interactive) or (re.match(regular, f) and (interactive and deleter.confirmed(f))):
				delete_to_trash([directory + '/'+f], location , trash_location)
		else:
			delete_to_trash_by_reg(regular, directory + '/' + f, location, trash_location, interactive)
