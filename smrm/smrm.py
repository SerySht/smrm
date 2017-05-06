import os
import sys
import trash
import argparse
import logging
import config


def main():     
    
    parser = argparse.ArgumentParser()      
    parser.add_argument('-st', '--show_trash', action='store_true')
    parser.add_argument('-wt', '--wipe_trash', action='store_true')
    parser.add_argument('--recover', nargs='*')
    parser.add_argument('--regular', nargs=2, type=str, help='-reg [regular] [directory]')
    parser.add_argument('--silent', action='store_true')   
    parser.add_argument('-i','--interactive', action='store_true')
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('files', nargs='*') 
    
    parser.add_argument('--trash_location')
    parser.add_argument('--log_location')
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
    if arguments.log_location:
        conf['log_location'] = arguments.log_location
   

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',filemode="w",filename=conf['log_location'],level=logging.DEBUG)
    logging.debug(arguments)

    t = trash.Trash(conf['trash_location'], 
                    current_directory, 
                    conf['storage_time'], 
                    conf['trash_maximum_size'], 
                    conf['recover_conflict'], 
                    arguments.silent, 
                    arguments.interactive, 
                    arguments.dry_run,
                    arguments.force)

    if arguments.files:
        t.delete_to_trash(arguments.files)  
    elif arguments.show_trash:      
        t.show_trash()
    elif arguments.wipe_trash:
        t.wipe_trash()
    elif arguments.regular:
        t.delete_to_trash_by_reg('\\' + arguments.reg[0], arguments.reg[1])
    elif arguments.recover:
        t.recover_from_trash(arguments.recover)
    else:
        print "Error! There are no parameters!"    

if __name__ == "__main__":
    main()
    