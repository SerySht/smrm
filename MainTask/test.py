import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-kek', nargs='?', default='')
parser.add_argument('bek', nargs='?', default='')

arguments = parser.parse_args(sys.argv[1:])
if arguments.kek == 'lel':  #to trash 
		print "kek"