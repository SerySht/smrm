import os
import sys
import shutil
import argparse

#shutil.move(sys.argv[1], sys.argv[2])
parser = argparse.ArgumentParser()
parser.add_argument('--file', default = "filetest")
parser.add_argument('--trash_location', default = 'testtrash')
parser.add_argument('command')

arguments = parser.parse_args(sys.argv[1:]) 
#print arguments.file
#print arguments.trash_location
#if arguments.command = 'cleantrash':


#print os.listdir("testtrash") 
#shutil.rmtree("testtrash")
os.mkdir("testtrash")