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

		Parameters for initializzations of Trash:
	    non-optional:
	        trash_path = path of trash
	    optional:
	        trash_maximum_size = maximum size of trash, default = False
	        storage_time = time of storaging files(in days), default = False
	        recover_conflict = what do if name conflice while restore file (replace/not_replace), default = 'not_replace'
	        interactive = turn on interactive mode, default = False
	        log_path = path of log file, default = home dir
	        silent = turn on silent mode, default = False
	        verbose = turn on verbose mode(commenting what is happening), default = False
	        dry_run = turn on dry mode (not appling changes), default = False
	        force = turn to force mode, default = False


		Example of working with Trash:
		    my_trash = Trash(trash_path = "/home/username/Trash", verbose=True)
		    my_trash.delete_trash("/home/username/file1")


	utils.py:
		This module contains utils for working of class Trash

	trashconfig.py:
		This module loads config file if it exists, if not - create and loads default config

