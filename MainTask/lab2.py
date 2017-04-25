import os
import sys
import trash
import deleter
import argparse
import logging
import ConfigParser



def main():	
	
	logging.basicConfig(format = u'%(message)s',filemode="w",filename='/home/sergey/labs/lab2/MainTask/smart_rm.log',level=logging.DEBUG)
	
	parser = argparse.ArgumentParser()
	
	
	#parser.add_argument('-t', nargs='*')   
	parser.add_argument('-st', '-show_trash', action='store_true')
	parser.add_argument('-wt', action='store_true')
	parser.add_argument('-recover', nargs='*')
	parser.add_argument('-reg', nargs=2, type=str, help='-reg [regular] [directory]')
	parser.add_argument('-silent', action='store_true')
	parser.add_argument('-i','-interactive', action='store_true')
	parser.add_argument('-dry_run', action='store_true')
	parser.add_argument('files', nargs='*')	

	#parser.add_argument('-i', nargs='*')
	parser.add_argument('-ir', nargs='?')          
	parser.add_argument('-r', nargs='?')	
	#parser.add_argument('-reg', nargs=2, type=str, help='-reg [regular] [directory]')
	
	
	try:
		arguments = parser.parse_args(sys.argv[1:],)
	except:   		
		print "There is no such parameter!"
		return

	current_directory = os.getcwd()

	conf = ConfigParser.RawConfigParser()            
	conf.read('/home/sergey/labs/lab2/MainTask/smart_rm.conf') #os.path.expanduser('~/.myapp.cfg')])
	trash_location = conf.get("main", "trash_location")	
	recover_conflict = conf.get("main", "recover_conflict")
	storage_time = conf.get("politics", "storage_time") * 1 * 3600 #86400
	trash_maximum_size = conf.get("politics", "trash_maximum_size")

	t = trash.Trash(trash_location, current_directory, storage_time, trash_maximum_size, recover_conflict, arguments.silent, arguments.i, arguments.dry_run)

	if not os.path.exists(trash_location):		
		os.mkdir(trash_location)	


	logging.debug("arguments: " + str(arguments))
	logging.debug("current_directory: " + str(current_directory))	


	if arguments.files:
		t.delete_to_trash(arguments.files)
	
	elif arguments.st:		
		t.show_trash()

	elif arguments.wt:
		t.wipe_trash()

	elif arguments.reg:
		t.delete_to_trash_by_reg('\\' + arguments.reg[0], arguments.reg[1])

	elif arguments.recover:
		t.recover_from_trash(arguments.recover)



	elif arguments.i:
		deleter.delete(arguments.i, interactive = True) 

	elif arguments.ir:
		deleter.recursive_delete(arguments.ir, interactive = True) 
	
	#elif arguments.reg:
		#deleter.delete_by_reg(arguments.reg[0], arguments.reg[1])
	
	elif arguments.r:
		deleter.recursive_delete(arguments.r)	
	else:
		print "Error! There are no parameters!"

	#t.check_trash()


if __name__ == "__main__":
    main()
    