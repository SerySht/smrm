import os
import sys
import trash
import argparse
import logging
import TrashConfigParser


def main():     
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('files', nargs='*', help='delete file(s)')     
    parser.add_argument('-st', '--show_trash', action='store_true', help='show trash')
    parser.add_argument('-wt', '--wipe_trash', action='store_true', help='wipe trash')
    parser.add_argument('-r','--recover', nargs='*', help='recover file(s)')
    parser.add_argument('-re','--regular', nargs=2, type=str, help='delete by regular in directory')
    parser.add_argument('--silent', action='store_true', help='silent mode')   
    parser.add_argument('-i','--interactive', action='store_true', help='interactive mode')
    parser.add_argument('-dry', action='store_true', help='dry run')
    parser.add_argument('-f', '--force', action='store_true', 'ignore nonexistent files"')
     
    
    parser.add_argument('--trash', help='trash path')
    parser.add_argument('--log', help='log path'
    parser.add_argument('--recover_conflict', help='recover policy')
    parser.add_argument('--storage_time', help='time policy')
    parser.add_argument('--trash_maximum_size', help='trash size policy')
    
    arguments = parser.parse_args(sys.argv[1:])    
    current_directory = os.getcwd()
    conf = config.load()
    
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
   
   

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',filemode="w",filename=conf['log_path'],level=logging.DEBUG)
    logging.info(arguments)

    my_trash = trash.Trash(conf['trash_path'], 
                    current_directory, 
                    conf['storage_time'], 
                    conf['trash_maximum_size'], 
                    conf['recover_conflict'], 
                    arguments.silent, 
                    arguments.interactive, 
                    arguments.dry_run,
                    arguments.force)

    if arguments.files:
        for f in arguments.files:
            my_trash.delete_to_trash(f) 
    
    elif arguments.recover:
        for f in arguments.recover:
            my_trash.recover_from_trash(f)   

    elif arguments.regular:
        my_trash.delete_to_trash_by_reg('\\' + arguments.reg[0], arguments.reg[1])    
    elif arguments.show_trash:      
        my_trash.show_trash()
    elif arguments.wipe_trash:
        my_trash.wipe_trash()
    else:
        print "Error! There are no parameters!"    

if __name__ == "__main__":
    main()
    