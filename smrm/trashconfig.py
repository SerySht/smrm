import ConfigParser
import json
import os


def load(directory = "smrm.conf"):

    if os.path.exists(directory):
        conf_dict = {}

        if os.path.splitext(directory)[1] == ".json":
            with open(directory, 'r') as config:
                conf_dict.load(config)
        else:
            conf = ConfigParser.RawConfigParser()            
            conf.read(directory)
            
            if conf.has_option("main", "trash_path"):
                conf_dict["trash_path"] = conf.get("main", "trash_path")        

            if conf.has_option("main", "log_path"):
                conf_dict['log_path'] = conf.get("main", "log_path")            
            
            if conf.has_option("main", "recover_conflict"):
                conf_dict['recover_conflict'] = conf.get("main", "recover_conflict")            
            
            if conf.has_option("politics", "storage_time"):
                conf_dict['storage_time'] = conf.get("politics", "storage_time") 
            
            if conf.has_option("politics", "trash_maximum_size"):
                conf_dict['trash_maximum_size'] = conf.get("politics", "trash_maximum_size")
            
            return conf_dict
    else:
        print "Config not found, using default parameters"
        return {}
   

               