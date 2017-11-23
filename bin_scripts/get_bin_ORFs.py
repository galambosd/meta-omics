#!/usr/bin/env python
# run in a directory named FS* that's in per_bin_metab

import os, glob, pickle, sys
from os import getcwd
from datetime import datetime

# open the bed file

time1 = int(datetime.now()[5])

try:
	bedName = glob.glob('*.a.bed')[0]
except IndexError:
	print "Sorry, couldn't find a bed file."
	sys.exit("Exiting script...")
	
bedFile = open(bedName, 'r')
bedLines = bedFile.readlines()
bedFile.close()
print 'Opening {0}/{1}'.format(getcwd()[-5:],bedName)

# open the bin_list file
binFile = open('bin_list.txt', 'r')
print 'Opening {0}/bin_list.txt...'.format(getcwd()[-5:])
lines = binFile.readlines()
binFile.close()
# make a list of the bins
bin_list =[]
for line in lines:
	bin_list.append(line.rstrip('\n'))
	


# for each bin in the bin_list...
for bin in bin_list:
	# open the contigs_name file
	print "Parsing {0}...".format(bin)
	contigsFile = open('{0}/{0}-contigs_names.txt'.format(bin), 'r')
	contigLines = contigsFile.readlines()
	contigsFile.close()
	# open a new outfile in the bin directory w/ appropriate name
	outFile = open('{0}/{0}-ORF_names.txt'.format(bin), 'w')
	# write a quicc message at the top
	outFile.write('The ORFs for {0} from {1}'.format(bin, getcwd()[-5:]))
	pickleFile = open('{0}/{0}-ORF_names.pickle'.format(bin), 'wb')
	# new ORF list
	ORF_list = []
	
	# for each contig in the contig names file...
	for contig in contigLines:
		contig = contig.rstrip('\n')
		# copy all the ORF names to the outfile that match
		for line in bedLines:
			cols = line.split('\t')
			if len(cols) == 1:
				continue
			contig_name = cols[0]
			ORF_name = cols[3].rstrip('\n')
			if contig_name == contig and '=' not in ORF_name:
				ORF_list.append(ORF_name)
				outFile.write(ORF_name+'\n')
		# add the ORF name to an appropriately named JSON thing, also in Bin directory
		# ignore ones w/ '=' in them (nf=*, don = *, etc)

	# dump the ORF list to the json file
	pickle.dump(ORF_list, pickleFile)
	pickleFile.close()
	outFile.close()
	
time2 = int(datetime.now()[5])
print 'Done. Runtime was {0}'.format(time2-time1)
