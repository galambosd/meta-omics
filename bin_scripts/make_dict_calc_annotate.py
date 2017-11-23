#!/usr/bin/env python
# run in a directory named FS* that's in per_bin_metab


import pickle, os, sys, glob
path = r'./'


# for each file ending in calculated_annotated_KO.txt...
for fileName in glob.glob(os.path.join(path, '*calculated_and_annotated_KO.txt')):
	D = {}
	# open the file, read the lines
	inFile = open(fileName, 'r')
	lines = inFile.readlines()
	inFile.close()
	# for each line in the file:
	for line in lines:
		# separate the columns
		cols = line.split('\t')
		D[cols[0]] = '\t{0}\t{1}'.format(cols[1], cols[2])  # the newline is kept bc cols[2] still has it
	# open a binary pickle outfile based on the the calc_annotated file
	outFile = open(fileName.rstrip('txt').lstrip('./')+'pickle', 'wb')
	# dump the dict
	print "Saving {0}...".format(outFile.name)
	pickle.dump(D, outFile)
	# close the file
	outFile.close()
		
# exact same thing for each pfam file
for fileName in glob.glob(os.path.join(path, '*calculated_and_annotated_pfam.txt')):
	D = {}
	# open the file, read the lines
	inFile = open(fileName, 'r')
	lines = inFile.readlines()
	inFile.close()
	# for each line in the file:
	for line in lines:
	# separate the columns
		cols = line.split('\t')
		D[cols[0]] = '\t{0}\t{1}'.format(cols[1], cols[2])  # the newline is kept bc cols[2] still has it
		# open a binary pickle outfile based on the the calc_annotated file
	outFile = open(fileName.rstrip('txt').lstrip('./')+'pickle', 'wb')
	# dump the dict
	print "Saving {0}...".format(outFile.name)
	pickle.dump(D, outFile)
	# close the file
	outFile.close()
		
print 'Done.'
