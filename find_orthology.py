#!/usr/bin/env python

import os, glob, argparse, pickle
from sys import argv
path = r'./'

# set up the arg parser / help messages

parser = argparse.ArgumentParser(description = 'Find and compile all the protein sequences of an ortholog.')

parser.add_argument('O_number', metavar = 'orthology number', help = 'The KO, pfam or COG number of the orthology you want to find. KO*, pfam* or COG*.')  

# take command line input of which orthology to find, pfam, KO or COG
# orthology = this number

# optionally take the "real" name of the orthology
parser.add_argument('-n', metavar = 'orthology name', help = 'A name to assign to the orthology number you enter (eg. SoxX, mcrA).')
	# if this happens, orthology == this name

args = parser.parse_args()
O_num = args.O_number
orthology = O_num
if args.n != None:
	orthology = args.n
	O_name = args.n
	

# if __ in file, extension == ___
if 'K' in O_num:
	type = 'KO'
elif 'pfam' in O_num:
	type = 'pfam'
elif 'COG' in O_num:
	type = 'COG'
else:
	raise Exception('Please enter a KO, pfam or COG number.')

# open an output faa file to put the ORFs into
outFile = open('{}.faa'.format(orthology), 'w')

logFile = open('{0}_log.txt'.format(orthology), 'w')

samples = pickle.load(open('/Accounts/galambosd/FS_list_DNA.txt.pickle', 'rb'))

# get all the self-self DNA ORF coverage txt files
for FS in samples:
	# get the sample number of current file
	# open the file and get the KO-matching ORFs
	inFile = open('{0}/{0}_reads_vs_MidCaymanRise_{0}_idba_ORF'.format(FS)+
	'_coverage_calculated_and_annotated_{0}.txt'.format(type), 'r')
	print inFile.name
	inLines = inFile.readlines()
	inFile.close()
	# go through file and add all ORFs matching orthology to a temporary list
	ORFs = []
	for line in inLines:
		cols = line.split('\t')
		if O_num in cols[1]:
			ORFs.append(cols[0])
	# open the sample-associated faa file
	faa_name = glob.glob('{0}/*.faa'.format(FS))[0]
	print '\t' + faa_name
	faa_file = open(faa_name, 'r')
	faa_lines = faa_file.readlines()
	# for every item in list ...
	for ORF in ORFs:
		# while not feof for faa file...
		for line in faa_lines:
			if '>' in line:
				if ORF == line.lstrip('>').rstrip('\n'):
					write = '>{0}_{1}_{2}'.format(FS, orthology, ORFs.index(ORF)+1)
					outFile.write(write+'\n')
					logFile.write(write + '\t' + ORF + '\n')
					target = True
				else:
					target = False
			elif target:
				outFile.write(line)

	
	#close the faa file
	faa_file.close()
	
# close output file
outFile.close()
logFile.close()
