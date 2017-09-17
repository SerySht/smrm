"""
This module loads config file if it exists, if not - create and loads default config
"""
import ConfigParser
import json
import os
import sys


class Defaults(object):
    """
    This class contains default paths
    """    
    TRASH_PATH = os.path.join(os.getenv('HOME'), "Trash")

    LOG_PATH = os.path.join(os.getenv('HOME'), 'smrm.log')

    CONFIG_PATH = os.path.join(os.getenv('HOME'), ".smrmconfig.json")

    CONFIG_DICT = {
            "trash_path": TRASH_PATH,
            "log_path": LOG_PATH,
            "silent": False,
            "recover_conflict": "not_replace",
            "storage_time": False,
            "trash_maximum_size": False,
            "verbose":False,               
            "force":False,
            "interactive":False,
            "dry_run":False, 
    }


def load_config(config_path=Defaults.CONFIG_PATH):
    """This function reads config file or loads defaults"""
    
    conf_dict = Defaults.CONFIG_DICT

    if config_path == Defaults.CONFIG_PATH:

        if os.path.exists(Defaults.CONFIG_PATH):
            with open(Defaults.CONFIG_PATH, 'r') as config:
                conf_dict.update(json.load(config))
        else:
            print "Warning: Creating default config"
            with open(Defaults.CONFIG_PATH, 'w') as config:
                config.write(json.dumps(conf_dict))

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

                if conf.has_option("main", "verbose"):
                    conf_dict['verbose'] = conf.get("main", "verbose")

                if conf.has_option("main", "interactivee"):
                    conf_dict['interactive'] = conf.get("main", "interactive")

                if conf.has_option("main", "force"):
                    conf_dict['force'] = conf.get("main", "force")

                if conf.has_option("main", "dry_run"):
                    conf_dict['dry_run'] = conf.get("main", "dry_run")

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

