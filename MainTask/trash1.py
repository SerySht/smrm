import os
import json
import shutil
import deleter
import time
import re
import logging


class Trash(object):

	def __init__ (self, tl, cd, storage_time, tms, rc, silent=False):
		self.trash_location = tl 
		self.current_directory = cd
		self.trash_maximum_size = tms
		self.recover_conflict = rc
		self.silent = silent 

	
	def load_from_filelist(self):	
		f = open(self.trash_location + "/filelist", 'a+')               
		try:
			self.d = json.load(f)
		except ValueError:
			self.d = {}  
		f.close() 		

	
	def save_to_filelist(self):
		f = open(self.trash_location + "/filelist", 'w')  
		f.write(json.dumps(self.d))
		f.close()

	
	def separate_the_name(self, filename):
		i = filename.rfind('/')	
		if i > 0: 
			return filename[0:i+1], filename[i+1:]
		return '', filename

	
	def can_be_deleted(self, filename):
		return os.access(filename, os.W_OK)


	def location_check(self, location, location_add):
		if location_add != '':
			if location_add.find(location) == 0:
				return location_add
			elif location_add[0] == '/':
				return location_add	
			return location + '/'+ location_add
		return location

	
	def to_trash_mover(self, filename):
		shutil.move(filename, self.trash_location + '/temporary')
		self.key = str(os.stat(self.trash_location + '/temporary/' + filename).st_ino)			
		os.rename(self.trash_location + '/temporary/' + filename, self.trash_location + '/' + self.key)


	def add_to_filelist(self):
		if self.d.get(self.f) == None:
			self.d[self.f] = [{'location':self.location_check(self.current_directory, self.location_add), 'key':self.key, 'time':str(time.time()), 'size':os.path.getsize(self.trash_location+'/' + self.key)}]
		else:
			self.d[self.f].append({'location':self.location_check(self.current_directory, self.location_add), 'key':self.key, 'time':str(time.time()),'size':os.path.getsize(self.trash_location+'/'+ self.key)})


	def add_slash(self, p):
		if p[0] != '/':
			return '/' + p
		return p


	def delete_to_trash(self, filenames):	

		self.load_from_filelist() 	

		for filename in filenames:
			self.location_add, self.f = self.separate_the_name(filename)	

			if self.can_be_deleted(filename):	
				
				self.to_trash_mover(filename)
				self.add_to_filelist()

				if not self.silent:
					print "\"{0}\" successfully moved to trash".format(self.f)	
			else:
				print self.f," can't be deleted!"
		


		self.save_to_filelist()
		

	def add_slash(self, p):
			if p[0] != '/':
				return '/' + p
			return p


	def conflict_solver(self, filename):
		if self.recover_conflict != 'replace':
			try:
				int(filename[filename.rfind('(')+1:filename.rfind(')')])
			except ValueError:
				return filename + '(1)'
			num = int(filename[filename.rfind('(')+1:filename.rfind(')')])
			return filename.replace(str(num), str(num+1))
	 	return filename				
		



	def recover_from_trash(filenames, trash_location, recover_conflict):
		
		load_from_filelist(trash_location)

		for filename in filenames:
			list_of_files = d.get(filename)				
			if list_of_files == None:
				print "There is no such file!!!"
				continue	
			
			else:
				if len(list_of_files) == 1:	
					if not os.path.exists(list_of_files[0]["location"] + '/' + filename):						
						os.rename(trash_location + '/' + list_of_files[0]['key'], list_of_files[0]["location"] + '/' + filename)
						d.pop(filename) 
					else: 
						os.rename(trash_location + '/' + list_of_files[0]['key'], conflict_solver(recover_conflict, list_of_files[0]["location"] + '/' + filename))
				else:
					print "Which one you want to recover?"	
					for i in range(len(list_of_files)):
						print "#{0} from {1} deleted at {2}".format(i+1, list_of_files[i]["location"], time.ctime(float(list_of_files[i]["time"])))
					number = int(raw_input()) - 1	
					
					if not os.path.exists(list_of_files[number]["location"] + '/' + filename):
						os.rename(trash_location + '/' + list_of_files[number]['key'], list_of_files[number]["location"] + '/' + filename)
					else:
						os.rename(trash_location + '/' + list_of_files[number]['key'], conflict_solver(recover_conflict, list_of_files[number]["location"] + '/' + filename))
					list_of_files.pop(number)
					d[filename] = list_of_files				

		save_to_filelist(trash_location, d)



	def wipe_trash(trash_location, silent = False):
		deleter.recursive_delete(trash_location)
		os.mkdir(trash_location)
		if not silent:
			print "Trash wiped!"



	def show_trash(trash_location):
		d = load_from_filelist(trash_location)
		if d != {}:
			for filename in d:		
				for f in d[filename]:
					print "\"{0}\" was deleted from: {1} at {2}".format(str(filename), f["location"],time.ctime(float(f["time"])))					
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
					logging.info("\"{0}\" will be deleted in {1} sec".format(filename, int(storage_time) - int(t - float(f['time']))))	
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
				