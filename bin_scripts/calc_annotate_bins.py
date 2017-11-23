#!/usr/bin/env python
# run in a directory named FS* that's in per_bin_metab

import os, glob, pickle, sys
from subprocess import call
from os import getcwd

# run the python script to make a pickle dict out of everything

call("python ~/own_scripts/bin_bubble/make_dict_calc_annotate.py", shell = True)

# open the bin_list file
binFile = open('bin_list.txt', 'r')
binLines = binFile.readlines()
binFile.close()

bin_list = []

for line in binLines:
	bin_list.append(line.rstrip('\n'))

# make a list of the bins in sample

# close bin_list file


# for each bin...
for bin in bin_list:
	print 'Parsing {0}'.format(bin)
	# for each pickle file...
	for fileName in glob.glob(os.path.join(path, '*.pickle')):
		print fileName
		# open in bin direct. outfile w/ the bin name in front followed by calculated_annotated name
		outFile = open("{0}/{0}-{1}.txt".format(bin, fileName.lstrip('./').rstrip('.pickle')), 'w')
		# open the ORF pickle
		ORFfile = open("{0}/{0}-ORF_names.pickle".format(bin), 'rb')
		ORF_list = pickle.load(ORFfile)
		ORFfile.close()
		# open the calculated_annotated pickle
		calc_annotated_file = open(fileName.lstrip('./'), 'rb')
		D_calc = pickle.load(calc_annotated_file)
		calc_annotated_file.close()
		# for each item in the ORF pickle....
		for ORF in ORF_list:
			outFile.write(ORF+D_calc[ORF])
			# get the ORF coverage line from the calculated_annotated pickle file
			# print it to the outfile
		# close outfile
		outFile.close()