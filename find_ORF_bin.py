#!/usr/bin/env python

import glob, os, argparse, pickle
path = r'./'

parser = argparse.ArgumentParser(description="Make labels for an iTOL tree annotation " 
+ "by connecting ORFs to a bin and taxonomy. Needs find_orthology.py log files, a bed "
+"file for each sample site, and a list of contigs for each bin.")

parser.add_argument('file', metavar = 'log_file', help = 'The find_orthology.py log file with the ORFs for a gene orthology.')

# bin search -- takes FS, contig
def bin_search(FS, contig):
	# search for the bin # 
	for fileName in glob.glob(os.path.join(path, '/Accounts/galambosd/bin_summary/{0}/*/*/*/*/Bin*-contigs.fa'.format(FS))):
		binFile = open(fileName, 'r')
		binLines = binFile.readlines()
		binFile.close()
		for line in binLines:
			if '>' not in line:
				continue
			if line.rstrip('\n').lstrip('>') == contig:
				shortFileName = fileName.split('/')
				shortFileNameSplit = shortFileName[-1].split('-')
				bin = shortFileNameSplit[0]
				return bin
	# returns a string with sample, taxonomy and bin # (W/O 'bin')

# search for a contig-- takes ORF, FS
def contig_search(FS, ORF):
	# open the bed file for the FS
	bedName = glob.glob('/Accounts/galambosd/bubble_plots/JGI_output_MCR_metagenome_assemblies/{0}/*.bed'.format(FS))[0]
	bedFile = open(bedName, 'r')
	print'Opening {0}...'.format(bedName)
	inLines = bedFile.readlines()
	# for each line of the bed file...
	for line in inLines:
		# split the lines
		# if the target ORF is in the lines, that's our contig
		cols = line.split('\t')
		if len(cols) == 1:
			continue
		if cols[3].rstrip('\n') == ORF:
			return cols[0]
	

# open the log file
args = parser.parse_args()
logFile = open(args.file, 'r')
logLines = logFile.readlines()
logFile.close()

outFile = open('iTOL_line_annotate.txt', 'w')

# open dict of FS+bin# --> taxonomy
D_file = open('/Accounts/galambosd/bin_summary/all_bins_taxonomy.pickle', 'rb')
D_tax = pickle.load(D_file)
D_file.close()

# for each line ...
for line in logLines:
	cols = line.split('\t')
	FS = cols[0][1:6]
	ORF = cols[1].rstrip('\n')
	print '{0} from {1}'.format(ORF, FS)
	# call function to search for a contig -- takes FS and ORF
	contig = contig_search(FS, ORF)
	# call function to search Bin_*-contigs.fa files, takes FS and contig
	bin = bin_search(FS, contig)
	key = '{0}_{1}'.format(FS, bin)
	# search for a FS_bin combo -- if the key exists, write the old combo 
	if key in D_tax:
		result = D_tax[key][0].lstrip("'").rstrip("'")
		outFile.write(cols[0].lstrip('>')+'\t'+'{0}_{1}_{2}'.format(FS, result, bin.lstrip('Bin_'))+'\n')
		# and new combo to outfile
	else:
		outFile.write('{0}\t{1}\n'.format(cols[0].lstrip('>'), key))
		
	#otherwise, just write the old combo twice

outFile.close()	
	

