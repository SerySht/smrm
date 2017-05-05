import ConfigParser
import json


def load(directory = '/home/sergey/labs/lab2/smrm/smrm.conf'):
	conf = ConfigParser.RawConfigParser()            
	conf.read(directory)
	
	if conf.has_option("main", "trash_location"):
		trash_location = conf.get("main", "trash_location")
 	else: 
 		trash_location = ''

 	if conf.has_option("main", "log_location"):
		log_location = conf.get("main", "log_location")
	else:
		log_location = ''
	
	if conf.has_option("main", "recover_conflict"):
		recover_conflict = conf.get("main", "recover_conflict")
	else: 
		recover_conflict = 'not_replace'	
	
	if conf.has_option("politics", "storage_time"):
		storage_time = conf.get("politics", "storage_time") 
	else: 
		storage_time = ''

	if conf.has_option("politics", "trash_maximum_size"):
		trash_maximum_size = conf.get("politics", "trash_maximum_size")
	else:
		trash_maximum_size = ''


	json_config = {'trash_location':trash_location,
					'log_location':log_location, 
					'recover_conflict':recover_conflict, 
					'storage_time':storage_time,
					'trash_maximum_size':trash_maximum_size}

	f = open(directory[:-4]+'json', 'a+')                
	f.write(json.dumps(json_config))

	return json_config			