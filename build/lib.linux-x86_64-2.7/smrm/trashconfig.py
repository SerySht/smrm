import ConfigParser
import json
import os

trash_path = os.path.join(os.getenv('HOME'), "Trash")
log_path =  os.path.join(trash_path,'smrm.log')
default_config_path = os.path.join(os.getenv('HOME'), ".smrmconfig.json")


conf_dict = {"trash_path": trash_path,
            "log_path": log_path,
            "silent": False,            
            "recover_conflict" : "not_replace",
            "storage_time": 7,
            "trash_maximum_size": 100000}


def load(config_path=default_config_path):   
        
    if not os.path.exists(config_path):       
        if os.path.exists(default_config_path):
            with open(default_config_path, 'r') as config:
                conf_dict.update(json.load(config))
        else:
            with open(default_config_path, 'w') as config:
                config.write(json.dumps(conf_dict))

    else:    
        if os.path.splitext(config_path)[1] == ".json":
            with open(config_path, 'r') as config:
                conf_dict.update(json.load(config))
        else:
            conf = ConfigParser.RawConfigParser()            
            conf.read(config_path)
            
            if conf.has_option("main", "trash_path"):
                conf_dict["trash_path"] = conf.get("main", "trash_path")        

            if conf.has_option("main", "log_path"):
                conf_dict['log_path'] = conf.get("main", "log_path")            

            if conf.has_option("main", "silent"):
                conf_dict['silent'] = conf.get("main", "silent")
           
            if conf.has_option("main", "recover_conflict"):
                conf_dict['recover_conflict'] = conf.get("main", "recover_conflict")            
            
            if conf.has_option("main", "storage_time"):
                conf_dict['storage_time'] = conf.get("main", "storage_time") 
            
            if conf.has_option("main", "trash_maximum_size"):
                conf_dict['trash_maximum_size'] = conf.get("main", "trash_maximum_size")
            

    return conf_dict
   

               