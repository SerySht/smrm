smart rm for Linux
"smrm"

INSTALL:
Write "sudo python setup.py instal" to install app 

AFTER INSTALL:
Write "smrm [parameter]"


@parameters
[filename], [filename1]..., [filenameN]   = deleting files     
-st  --show_trash                         = show trash
-wt  --wipe_trash                         = wipe trash
-r  --recover                             = recover file(s)
-regex                                    = delete by regex in directory
--silent                                  = silent mode 
-i  --interactive'                        = interactive mode
-dry                                      = dry run
-f   --force                              = ignore nonexistent files
-v   --verbose                            = explain the actions
-dry --dry_run 	                          = dry run mode (shows what will be done but not applying changes)
     
--config_path                             = config path
--trash_path                              = trash path
--log_pat                                 = log path
--recover_conflict                        = recover policy
--storage_time'                           = time policy
--trash_maximum_size                      = trash size policy



MODULES:
	argparser.py:
	gets argumets from console and calls trash module

	trash.py:
	Module contains class Trash, which serves for creation and manipulation with trashes

	utils.py:
	This module contains utils for working of class Trash

	trashconfig.py:
	This module loads config file if it exists, if not - create and loads default config

