import os
import sys
import trash
import argparse
import logging
import trashconfig
from utils import output


def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument('files', nargs='*', help='delete file(s)')     
    parser.add_argument('-st', '--show_trash', nargs="?", const="0", help='show trash')
    parser.add_argument('-wt', '--wipe_trash', action='store_true', help='wipe trash')
    parser.add_argument('-r','--recover', nargs='*', help='recover file(s)')
    parser.add_argument('-re','--regex', nargs=2, type=str, help='delete by regex in directory')
    parser.add_argument('--silent', action='store_true', help='silent mode')   
    parser.add_argument('-i','--interactive', action='store_true', help='interactive mode')
    parser.add_argument('-dry', action='store_true', help='dry run')
    parser.add_argument('-f', '--force', action='store_true', help='ignore nonexistent files"')
     
    parser.add_argument('--config', help='config path')
    parser.add_argument('--trash', help='trash path')
    parser.add_argument('--log', help='log path')
    parser.add_argument('--recover_conflict', help='recover policy')
    parser.add_argument('--storage_time', help='time policy')
    parser.add_argument('--trash_maximum_size', help='trash size policy')
   
    arguments = parser.parse_args(sys.argv[1:])
    
    if arguments.config:
        conf = trashconfig.load(arguments.config)
    else:
        conf = trashconfig.load()    
    if arguments.trash:
        conf['trash_path'] = arguments.trash
    if arguments.log:
        conf['log_path'] = arguments.log
    if arguments.recover_conflict:
        conf['recover_conflict'] = arguments.recover_conflict
    if arguments.storage_time:
        conf['storage_time'] = arguments.storage_time
    if arguments.trash_maximum_size:
        conf['trash_maximum_size'] = arguments.trash_maximum_size   
   
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',filemode="w",
                                filename=conf['log_path'], level=logging.DEBUG)
    logging.debug(arguments)

    my_trash = trash.Trash(conf['trash_path'], 
                            os.getcwd(), 
                            conf['storage_time'], 
                            conf['trash_maximum_size'], 
                            conf['recover_conflict'], 
                            conf['silent'], 
                            arguments.interactive, 
                            arguments.dry,
                            arguments.force)
    
    output_data = []
    if arguments.files:        
        for f in arguments.files:
            output_data.append(my_trash.delete_to_trash(f))
        output(output_data)

    elif arguments.recover:
        for f in arguments.recover:
            output_data.append(my_trash.recover_from_trash(f))
        output(output_data)

    elif arguments.regex:
        output_data.append(my_trash.delete_to_trash_by_reg('\\' + arguments.regex[0], arguments.regex[1]))  
    
    elif arguments.show_trash:      
        output(my_trash.show_trash(int(arguments.show_trash)))
    
    elif arguments.wipe_trash:
        output(my_trash.wipe_trash())
    else:
        print "No arguments"
    my_trash.policy_check()


if __name__ == "__main__":
    main()
      
    