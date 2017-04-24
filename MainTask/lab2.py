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
	
	parser.add_argument('files', nargs='*')	
	#parser.add_argument('-t', nargs='*')   
	parser.add_argument('-st', '-show_trash', action='store_true')
	parser.add_argument('-wt', action='store_true')
	parser.add_argument('-recover', nargs='*')

	parser.add_argument('-i', nargs='*')
	parser.add_argument('-ir', nargs='?')          
	parser.add_argument('-r', nargs='?')
	parser.add_argument('-silent', action='store_true')
	parser.add_argument('-reg', nargs=2, type=str, help='-reg [regular] [directory]')
	parser.add_argument('-reg_t', nargs=2, type=str, help='-reg [regular] [directory]')
	
	try:
		arguments = parser.parse_args(sys.argv[1:],)
	except:   		
		print "There is no such parameter!"
		return

	location = os.getcwd()

	conf = ConfigParser.RawConfigParser()            
	conf.read('/home/sergey/labs/lab2/MainTask/smart_rm.conf') #os.path.expanduser('~/.myapp.cfg')])
	trash_location = conf.get("main", "trash_location")
	storage_time = conf.get("main", "storage_time")
	trash_maximum_size = conf.get("main", "trash_maximum_size")
	recover_conflict = conf.get("main", "recover_conflict")

	t = trash.Trash(trash_location, location, storage_time, trash_maximum_size, recover_conflict, silent=False)


	storage_time = int(storage_time) * 1 * 3600 #86400
	logging.info(storage_time)

	if not os.path.exists(trash_location):		
		os.mkdir(trash_location)	


	logging.debug("arguments: " + str(arguments))
	logging.debug("location: " + str(location))	


	if arguments.files:
		t.delete_to_trash(arguments.files)

	#elif arguments.t:       
		#trash.delete_to_trash(arguments.t, location, trash_location, arguments.silent)

	elif arguments.st:		
		t.show_trash()

	elif arguments.wt:
		t.wipe_trash()

	elif arguments.recover:
		t.recover_from_trash(arguments.recover)

	elif arguments.i:
		deleter.delete(arguments.i, interactive = True) 

	elif arguments.ir:
		deleter.recursive_delete(arguments.ir, interactive = True) 
	
	elif arguments.reg:
		deleter.delete_by_reg(arguments.reg[0], arguments.reg[1])
	
	elif arguments.r:
		deleter.recursive_delete(arguments.r)	
	elif arguments.reg_t:
		t.delete_to_trash_by_reg('\\' + arguments.reg_t[0], arguments.reg_t[1], location, trash_location)
	else:
		print "Error! There are no parameters!"

	t.check_trash()


if __name__ == "__main__":
    main()
    