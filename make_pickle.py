#!/usr/bin/env python

import argparse, sys, pickle

parser = argparse.ArgumentParser(description = 'Turn a tab-separated text file into a Pickled list (1 column) or dict (multiple columns).')
parser.add_argument('t', metavar = 'Object Type', choices = ['list', 'dict'], help = 'Choose to turn your file into a list or a dict.')
parser.add_argument('f', metavar = 'Input File', help = 'Provide the path of your input file.')
parser.add_argument('-o', metavar = 'Output File', help = "Specify the name for your '*.pickle' outfile.")

args = parser.parse_args()

try:
	inFile = open(args.f, 'r')
	inLines = inFile.readlines()
	inFile.close()
except IOException():
	print 'Sorry, {0} could not be found.'.format(args.f)
	sys.exit()

if args.t == 'list':
	O = []
	for line in inLines:
		O.append(line.rstrip('\n'))
	print 'Created a Pickled list with {0} items.'.format(len(O))

else:
	O = {}
	for line in inLines:
		cols = line.split('\t')
		cols[-1]= cols[-1].rstrip('\n')
		O[cols[0]]= cols[1:]
	print 'Created a Pickled dictionary with {0} keys.'.format(len(O))
	
if args.o != None:
	outFile = open('{0}.pickle'.format(args.o), 'wb')
else:
	outFile = open('{0}.pickle'.format(inFile.name), 'wb')
	
pickle.dump(O, outFile)

outFile.close()
print 'Done.'
		

	
	
	
