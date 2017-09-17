"""
This module for working with console
"""
import os
import sys
import argparse
import logging
from smrm.trash import Trash
from smrm.utils import output
from smrm.trashconfig import load_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='delete file(s)')
    parser.add_argument('-st', '--show_trash', nargs="?", const="0", help='show trash')
    parser.add_argument('-wt', '--wipe_trash', action='store_true', help='wipe trash')
    parser.add_argument('-r', '--recover', nargs='*', help='recover file(s)')
    parser.add_argument('-regex', '--regex', nargs=2, type=str, help='delete by regex in directory')
    parser.add_argument('-s','--silent', action='store_true', help='silent mode')
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive mode')
    parser.add_argument('-dry', '--dry_run', action='store_true', help='dry run')
    parser.add_argument('-f', '--force', action='store_true', help='ignore nonexistent files')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')

    parser.add_argument('--config_path', help='config path')
    parser.add_argument('--trash_path', help='trash path')
    parser.add_argument('--log_path', help='log path')
    parser.add_argument('--recover_conflict', help='recover policy')
    parser.add_argument('--storage_time', help='time policy')
    parser.add_argument('--trash_maximum_size', help='trash size policy')

    arguments = parser.parse_args(sys.argv[1:])

    if arguments.config_path:
        conf = load_config(arguments.config_path)
    else:
        conf = load_config()
    if arguments.silent:
        conf['silent'] = True
    if arguments.verbose:
        conf['verbose'] = True 
    if arguments.force:
        conf['force'] = True 
    if arguments.interactive:
        conf['interactive'] = True 
    if arguments.dry_run:
        conf['dry_run'] = True    
    if arguments.trash_path:
        conf['trash_path'] = arguments.trash_path
    if arguments.log_path:
        conf['log_path'] = arguments.log_path
    if arguments.recover_conflict:
        conf['recover_conflict'] = arguments.recover_conflict
    if arguments.storage_time:
        conf['storage_time'] = arguments.storage_time
    if arguments.trash_maximum_size:
        conf['trash_maximum_size'] = arguments.trash_maximum_size

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filemode="w",
                        filename=conf['log_path'], level=logging.DEBUG)
    logging.debug(arguments)

    my_trash = Trash(**conf)

    output_data = []
    if arguments.files:
        output_data = my_trash.delete_to_trash(arguments.files)

    elif arguments.recover:
        for f in arguments.recover:
            output_data.append(my_trash.recover_from_trash(f))

    elif arguments.regex:        
        output_data = my_trash.delete_to_trash_by_reg('\\' + arguments.regex[0], arguments.regex[1])       

    elif arguments.show_trash:
        output_data = my_trash.show_trash(int(arguments.show_trash))

    elif arguments.wipe_trash:
        output_data = my_trash.wipe_trash()

    else:
        output_data = [("No arguments", 2)]
  
    output(output_data)


if __name__ == "__main__":
    main()
