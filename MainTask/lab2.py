import os
import sys
import trash
import deleter
import argparse
import logging
import ConfigParser


def main():	
	
	logging.basicConfig(filename='smart_rm.log',level=logging.DEBUG)
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('files', nargs='*')	
	parser.add_argument('-t', nargs='*')   
	parser.add_argument('-st', action='store_true')
	parser.add_argument('-wt', action='store_true')
	parser.add_argument('-recover', nargs='*')

	parser.add_argument('-i', nargs='*')
	parser.add_argument('-ir', nargs='?')             #make for list
	parser.add_argument('-r', nargs='?')
	parser.add_argument('-silent', action='store_true')
	parser.add_argument('-reg', nargs=2, type=str, help='-reg [regular] [directory]')
	
	try:
		arguments = parser.parse_args(sys.argv[1:],)
	except:   		
		print "There is no such parameter!"
		return

	location = os.getcwd() 

	logging.info(arguments)
	print arguments
	logging.info(location)	
	
	conf = ConfigParser.RawConfigParser()            
	conf.read("smart_rm.conf")
	trash_location = conf.get("main", "trash_location")
	storage_time = conf.get("main", "storage_time")
	
	if not os.path.exists(trash_location):		
		os.mkdir(trash_location)	


	if arguments.files:
		deleter.delete(arguments.files)
	elif arguments.t:       
		trash.delete_to_trash(arguments.t, location, trash_location, arguments.silent)
	elif arguments.st:
		trash.show_trash(trash_location)

	elif arguments.wt:
		trash.wipe_trash(trash_location)

	elif arguments.recover:
		trash.recover_from_trash(arguments.recover, trash_location)

	elif arguments.i:
		deleter.delete(arguments.i, interactive = True) 

	elif arguments.ir:
		deleter.recursive_delete(arguments.ir, interactive = True) 
	
	elif arguments.reg:
		deleter.delete_by_reg(arguments.reg[0], arguments.reg[1])
	
	elif arguments.r:
		deleter.recursive_delete(arguments.r)	
	else:
		print "Error! There are no parameters!"

	trash.check_trash(trash_location, storage_time)

main()
