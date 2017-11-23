#!/usr/bin/env python
import os, glob
path = r'./'

# open the contigs fasta files and join the paths in a list

# for each file

print 'Found these FASTA files:'
for fileName in glob.glob(os.path.join(path, '*.fa')):
	print fileName
	# open it
	inFile = open(fileName, 'r')
	# open a corresponding outfile
	outFile = open(fileName.rstrip('.fa')+'_names.txt', 'w')
	outFile.write('List of original contig names in {0}:\n'.format(fileName))
	lines = inFile.readlines()
	# each time a '>' is encountered, write the contig name to the outfile
	for line in lines:
		if line[0] == '>':
			outFile.write(line.lstrip('>'))
	# close the outfile
	outFile.close()
	# close the infile
	inFile.close()
	
print 'Done.'
