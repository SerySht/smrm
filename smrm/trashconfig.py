import ConfigParser
import json
import os


def load(directory):

    if not os.path.exists(directory):
           
    if os.path.splitext(directory)[1] == ".json":
        with open(directory, 'r') as config:
            d.load(config)
    else:
        conf = ConfigParser.RawConfigParser()            
        conf.read(directory)
        d = {}
        
        if conf.has_option("main", "trash_path"):
            d["trash_path"] = conf.get("main", "trash_path")
        else: 
            d["trash_path"] = os.path.join(os.getenv("HOME"), "Trash")

        if conf.has_option("main", "log_path"):
            d['log_path'] = conf.get("main", "log_path")
        else:
            d['log_path'] = os.path.join(os.getenv("HOME"), 'smrm.log')
        
        if conf.has_option("main", "recover_conflict"):
            d['recover_conflict'] = conf.get("main", "recover_conflict")
        else: 
            d['recover_conflict'] = 'not_replace'    
        
        if conf.has_option("politics", "storage_time"):
            d['storage_time'] = conf.get("politics", "storage_time") 
        else: 
            d['storage_time'] = ''

        if conf.has_option("politics", "trash_maximum_size"):
            d['trash_maximum_size'] = conf.get("politics", "trash_maximum_size")
        else:
            d['trash_maximum_size'] = ''

    return d          