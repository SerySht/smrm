import ConfigParser
import json


def load(directory = '/home/sergey/labs/lab2/MainTask/smrm.conf'):
	conf = ConfigParser.RawConfigParser()            
	conf.read(directory) 
	
	trash_location = conf.get("main", "trash_location")	
	recover_conflict = conf.get("main", "recover_conflict")
	storage_time = conf.get("politics", "storage_time") * 1 * 3600 #86400
	trash_maximum_size = conf.get("politics", "trash_maximum_size")

	json_config = {'trash_location':trash_location, 
					'recover_conflict':recover_conflict, 
					'storage_time':storage_time,
					'trash_maximum_size':trash_maximum_size}

	f = open(directory[:-4]+'json', 'a+')                
	f.write(json.dumps(json_config))

	return json_config			