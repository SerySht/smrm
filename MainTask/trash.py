import os
import json
import shutil
import deleter
import time
import re
import logging


class Trash(object):

	def __init__ (self, trash_location, current_directory, storage_time, trash_maximum_size, recover_conflict, silent=False):
		self.trash_location = trash_location 
		self.current_directory = current_directory
		self.trash_maximum_size = trash_maximum_size
		self.recover_conflict = recover_conflict
		self.silent = silent 

	
	def __load_from_filelist(self):	
		f = open(self.trash_location + "/parameters/filelist", 'a+')               
		try:
			self.dict = json.load(f)
		except ValueError:
			self.dict = {}  
		f.close() 		

	
	def __save_to_filelist(self):
		f = open(self.trash_location + "/parameters/filelist", 'w')  
		f.write(json.dumps(self.dict))
		f.close()		

	
	def delete_to_trash(self, filenames):

		def separate_the_name(filename):
			i = filename.rfind('/')	
			if i > 0: 
				return filename[:i+1], filename[i+1:]
			return '', filename

		def can_be_deleted(filename):
			return os.access(filename, os.W_OK)

		def location_check(current_directory, file_location):
			if file_location != '':
				if file_location.find(current_directory) == 0:
					return file_location
				elif file_location[0] == '/':
					return file_location	
				return current_directory + '/' + file_location
			return current_directory
		
		def to_trash_mover(filename):			
			self.key = str(os.stat(filename).st_ino)			
			os.rename(filename, self.trash_location + '/' + self.key)

		def add_to_filelist():
			self.__load_from_filelist() 	
			if self.dict.get(self.file) == None:
				self.dict[self.file] = [{'location':location_check(self.current_directory, self.file_location), 
											'key':self.key, 
											'time':str(time.time()), 
											'size':os.path.getsize(self.trash_location+ '/' + self.key)}]
			else:
				self.dict[self.file].append({'location':location_check(self.current_directory, self.file_location), 
											'key':self.key, 'time':str(time.time()),
											'time':str(time.time()),
											'size':os.path.getsize(self.trash_location+'/'+ self.key)})
			self.__save_to_filelist()	

		for filename in filenames:
			self.file_location, self.file = separate_the_name(filename)	

			if can_be_deleted(filename):				
				to_trash_mover(filename)
				add_to_filelist()
				
				if not self.silent:
					print "\"{0}\" successfully moved to trash".format(self.file)	
			else:
				print self.file," can't be deleted!"


	def recover_from_trash(self, filenames):

		def get_which_one():
			print "Which one you want to recover?"	
			for i in range(len(self.list_of_files)):
				print "#{0} from {1} deleted at {2}".format(i+1, self.list_of_files[i]["location"], time.ctime(float(self.list_of_files[i]["time"])))
			return int(raw_input()) - 1	

		def conflict_solver(filename):
			if self.recover_conflict != 'replace':
				try:
					int(filename[filename.rfind('(')+1:filename.rfind(')')])
				except ValueError:
					return filename + '(1)'

				num = int(filename[filename.rfind('(')+1:filename.rfind(')')])
				return filename.replace(str(num), str(num+1))
		 	return filename				

		def mover_from_trash(i, filename):	#pustie spiski
			if not os.path.exists(self.list_of_files[i]["location"] + '/' + filename):
				os.rename(self.trash_location + '/' + self.list_of_files[i]['key'], 
						self.list_of_files[i]["location"] + '/' + filename)				
			else:
				new_filename = self.list_of_files[i]["location"] + '/' + filename
				while os.path.exists(new_filename): 
					new_filename = conflict_solver(new_filename)
				
				os.rename(self.trash_location + '/' + self.list_of_files[i]['key'], new_filename)
			
			self.list_of_files.pop(i)   

		
		self.__load_from_filelist()

		for filename in filenames:
			self.list_of_files = self.dict.get(filename)				
			if self.list_of_files == None:
				print "There is no such file!!!"
				continue	
			
			else:
				if len(self.list_of_files) == 1:
					mover_from_trash(0, filename)					
				else:					
					self.get_which_one()					
					self.mover_from_trash(self.get_which_one(), filename)

				self.dict[filename] = self.list_of_files				

		self.__save_to_filelist()


	def wipe_trash(self):
		deleter.recursive_delete(self.trash_location)
		os.mkdir(self.trash_location)
		if not self.silent:
			print "Trash wiped!"


	def show_trash(self):
		self.__load_from_filelist()
		if self.dict != {}:
			for filename in self.dict:		
				for f in self.dict[filename]:
					print "\"{0}\" was deleted from: {1} at {2}".format(str(filename), f["location"],time.ctime(float(f["time"])))					
		else:	
			print "Trash is empty!"


	def time_politic_check(self):
		self.load_from_filelist()		
		t = time.time()
		copy_of_dict = self.dict.copy()
		for filename in self.dict:	
			i = -1	
			for f in self.dict[filename]:
				i += 1
				if (t - float(f['time'])) > int(self.storage_time):				
					os.remove(self.trash_location + '/' + f["key"])
					copy_of_dict[filename].pop(i) 	
					if len(copy_of_dict[filename]) == 0:
						copy_of_dict.pop(filename)
				else:				
					logging.info("\"{0}\" will be deleted in {1} sec".format(filename, int(self.storage_time) - int(t - float(f['time']))))	
		self.dict = copy_of_dict
		self.save_to_filelist()

	
	def delete_to_trash_by_reg(self, regular, directory, interactive = False):		
		files = os.listdir(directory)
		for f in files:		
			if not os.path.isdir(directory + '/' + f): 			
				if (re.match(regular, f) and not interactive) or (re.match(regular, f) and (interactive and deleter.confirmed(f))):
					self.delete_to_trash([directory + '/'+f])
			else:
				self.delete_to_trash_by_reg(regular, directory + '/' + f, interactive)
				
				