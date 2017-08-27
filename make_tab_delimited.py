#!/usr/bin/env python

# make a tab-delimited file from standard input or a file
import sys

def read_file(outFileName):
	fileName = raw_input("What file do you want to read? ")
	inFile = open(fileName, 'r')
	lines = inFile.readlines()
	inFile.close()
	if write:
		outFile = open(outFileName,'w')
	else:
		outFile = open(outFileName, 'a')
	delim = raw_input("What is the delimiter (at least press space)?" )
	print "Removing whitespace..."
	for line in lines:
		cols = line.split(delim)
		for col in cols[:-1]:
			col = col.lstrip().rstrip()
			outFile.write(col + '\t')
		cols[-1] = cols[-1].lstrip().rstrip()
		outFile.write(cols[-1] + '\n')
	print "Made a tab-delimited file {0} from {1}.".format(outFileName, fileName)
	
def read_input(outFileName):
	if write:
		outFile = open(outFileName,'w')
	else:
		outFile = open(outFileName, 'a')
	delim = raw_input("What is the delimiter (at least press space)? ")
	print "Enter data so that each line in stdin corresponds to a line in the outfile:"
	line = raw_input()
	while ('END' not in line):
		cols = line.split(delim)
		for col in cols[:-1]:
			col = col.lstrip().rstrip()
			outFile.write(col + '\t')
		cols[-1] = cols[-1].lstrip().rstrip()
		outFile.write(cols[-1] + '\n')
		line = raw_input()
	print "Made a tab-delimited file {0} from keyboard input.".format(outFileName)

write = False
if 'w' in sys.argv[1]:
	write = True
	
if  'in' in  sys.argv[2]:
	read_input(sys.argv[3])
else:
	read_file(sys.argv[3])
