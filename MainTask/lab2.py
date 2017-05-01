import os
import sys
import trash
import deleter
import argparse
import logging
import config



def main():	
	
	logging.basicConfig(format = u'%(message)s',filemode="w",filename='/home/sergey/labs/lab2/MainTask/smart_rm.log',level=logging.DEBUG)
	
	parser = argparse.ArgumentParser()	
	
	  
	parser.add_argument('-st', '-show_trash', action='store_true')
	parser.add_argument('-wt', action='store_true')
	parser.add_argument('-recover', nargs='*')
	parser.add_argument('-reg', nargs=2, type=str, help='-reg [regular] [directory]')
	parser.add_argument('-silent', action='store_true')
	parser.add_argument('-i','-interactive', action='store_true')
	parser.add_argument('-dry_run', action='store_true')
	parser.add_argument('files', nargs='*')	
	
	parser.add_argument('--trash_location')
	parser.add_argument('--recover_conflict')
	parser.add_argument('--storage_time')
	parser.add_argument('--trash_maximum_size')
	
	try:
		arguments = parser.parse_args(sys.argv[1:],)
	except:   		
		print "There is no such parameter!"
		return


	current_directory = os.getcwd()

	conf = config.load()
	
	if arguments.trash_location:
		conf['trash_location'] = arguments.trash_location
	if arguments.recover_conflict:
		conf['recover_conflict'] = arguments.recover_conflict
	if arguments.storage_time:
		conf['storage_time'] = arguments.storage_time
	if arguments.trash_maximum_size:
		conf['trash_maximum_size'] = arguments.trash_maximum_size

	t = trash.Trash(conf['trash_location'], current_directory, int(conf['storage_time']) * 3600, conf['trash_maximum_size'], conf['recover_conflict'], arguments.silent, arguments.i, arguments.dry_run)

	
	if not os.path.exists(conf['trash_location']):		
		os.mkdir(conf['trash_location'])	


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
	else:
		print "Error! There are no parameters!"

	t.time_politic_check()


if __name__ == "__main__":
    main()
    