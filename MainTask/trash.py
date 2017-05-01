import os
import json
import shutil
import deleter
import time
import re
import logging


class Trash(object):

	def __init__ (self, trash_location, current_directory, storage_time, trash_maximum_size, recover_conflict, silent, i, dry_run):
		self.trash_location = trash_location 
		self.current_directory = current_directory	
		self.storage_time = int(storage_time)	
		self.trash_maximum_size = trash_maximum_size
		self.recover_conflict = recover_conflict
		self.silent = silent 
		self.interactive = i
		self.dry_run = dry_run 
	
	def __load_from_filelist(self):	
		f = open(self.trash_location + "/filelist", 'a+')               
		try:
			self.dict = json.load(f)
		except ValueError:
			self.dict = {}  
		f.close() 		

	def __save_to_filelist(self):
		f = open(self.trash_location + "/filelist", 'w')  
		f.write(json.dumps(self.dict))
		f.close()		

	def __confirmed(self, filename):		
		while True:
			answer = raw_input("-Are you sure you want to move \"{0}\" to the Trash?\n".format(filename))
			if answer in {'yes', 'Yes', 'y', 'YES' 'da'}:
				return True
			elif answer in {'No', 'no', 'NO', 'net', 'n'}:
				return False
			else: print "Unknown answer"

	def __get_size(self, filename):
		if not os.path.isdir(filename):
			return os.path.getsize(filename)
		total_size = 0
		for r, d, files in os.walk(filename):
			for f in files:				
				total_size += os.path.getsize(r+'/'+f)
		return total_size
		
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
			self.size_politic_check(filename)

			self.key = str(os.stat(filename).st_ino)			
			os.rename(filename, self.trash_location + '/' + self.key)

		def add_to_filelist():
			self.__load_from_filelist() 	
			if self.dict.get(self.file) == None:
				self.dict[self.file] = [{'location':location_check(self.current_directory, self.file_location), 
											'key':self.key, 
											'time':str(time.time()), 
											'size':self.__get_size(self.trash_location+ '/' + self.key)}]
			else:
				self.dict[self.file].append({'location':location_check(self.current_directory, self.file_location), 
											'key':self.key, 'time':str(time.time()),
											'time':str(time.time()),
											'size':self.__get_size(self.trash_location+'/'+ self.key)})
			self.__save_to_filelist()	

		for filename in filenames:
			self.file_location, self.file = separate_the_name(filename)	
			if can_be_deleted(filename) and ((self.interactive and self.__confirmed(self.file)) or not self.interactive):
				if not self.dry_run:
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
					if not self.dry_run: mover_from_trash(0, filename)	
					else: print filename, "recovered from the trash"				
				else:										
					if not self.dry_run: mover_from_trash(get_which_one(), filename)
					else: 
						get_which_one()
						print filename, "recovered from the trash"

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
					print "\"{0}\" was deleted from: {1} at {2}".format(str(filename), f["location"], time.ctime(float(f["time"])))					
				
		if not self.silent:	
			print "Trash is empty!"


	def time_politic_check(self):
		self.__load_from_filelist()			
		
		for filename in self.dict:	
			for i in range(len(self.dict[filename])):	
				lists_by_name = self.dict[filename]
				if (time.time() - float(lists_by_name[i]['time'])) > self.storage_time:				
					if not os.path.isdir(self.trash_location + '/' + lists_by_name[i]["key"]):
						os.remove(self.trash_location + '/' + lists_by_name[i]["key"])
					else: shutil.rmtree(self.trash_location + '/' + lists_by_name[i]["key"])					
					self.dict[filename].pop(i)	
		self.__save_to_filelist()


	def size_politic_check(self, filename):
		size_of_trash = self.__get_size(self.trash_location)		
		if size_of_trash + self.__get_size(filename) > int(self.trash_maximum_size):			
			self.wipe_trash()



	def delete_to_trash_by_reg(self, regular, directory):
		p = Progress(directory)

		for r, d, files in os.walk(directory):
			for f in files:				
				if (re.match(regular, f) and not self.interactive) or (re.match(regular, f) and (self.interactive and self.__confirmed(f))):
					p.inc()					
					self.delete_to_trash([r + '/'+ f])
			p.show()			
		
		


class Progress(object):
	def __init__ (self, filename):
		self.num = 0
		self.all_ = sum([len(files) + len(d) for r, d, files in os.walk(filename)])
		self.proc = 0

	def inc(self):
		self.num += 1	

	def show(self):
		if self.proc != int((float(self.num) / self.all_) * 100):
			self.proc = int((float(self.num) / self.all_) * 100)
			print str(self.proc) + '%'