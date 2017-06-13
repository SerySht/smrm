import ConfigParser
import json
import os
import sys


class Default(object):
    trash_path = os.path.join(os.getenv('HOME'), "Trash")  
    log_path =  os.path.join(os.getenv('HOME'),'smrm.log')  
    config_path = os.path.join(os.getenv('HOME'), ".smrmconfig.json")
    conf_dict = {"trash_path": trash_path,
                "log_path": log_path,
                "silent": False,            
                "recover_conflict" : "not_replace",
                "storage_time": False,
                "trash_maximum_size": False}


def load(config_path=Default.config_path):
    conf_dict = Default.conf_dict 

    if config_path == Default.config_path:
        
        if os.path.exists(Default.config_path):
            with open(Default.config_path, 'r') as config:
                Default.conf_dict.update(json.load(config))
        else:
            print "Creating default config"
            with open(Default.config_path, 'w') as config:
                config.write(json.dumps(Default.conf_dict))

    else:
        if not os.path.exists(config_path): 
            print "Wrong config path"
            sys.exit(3)        
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
                    if conf.get("main", "storage_time").isdigit():
                        conf_dict['storage_time'] = int(conf.get("main", "storage_time"))
                    else:
                        conf_dict['storage_time'] = False
                    
                
                if conf.has_option("main", "trash_maximum_size"):
                    if conf.get("main", "trash_maximum_size").isdigit(): 
                        conf_dict['trash_maximum_size'] = int(conf.get("main", "trash_maximum_size"))
                    else:
                        conf_dict['trash_maximum_size'] = False                

    return conf_dict  

               