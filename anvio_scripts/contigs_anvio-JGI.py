#!/usr/bin/env python 

# make a pickle dictionary of

import pickle, argparse, os, glob

parser = argparse.ArgumentParser(description = 'Make a Pickle dictionary of anvio contig name (c_*) to JGI name (Ga*_*) using FS*_report_file.txt and *.map.txt files.')

parser.add_argument('d_list', metavar = 'DIRECTORIES_PICKLE', type = argparse.FileType('rb'), help = 'Path of the Pickled list of directories for the script to access.')

args = parser.parse_args()

d_list = pickle.load(args.d_list)
args.d_list.close()

def shortcut(FS, lines):
	D_anvio_JGI = {}
	for line in lines:
		cols = line.split('\t')
		D_anvio_JGI[cols[0]] = cols[1].rstrip('\n')
	return D_anvio_JGI
		
		
		
def longway(FS, lines):
	D_assembler_JGI = {}
	for line in lines:
		cols = line.split('\t')
		D_assembler_JGI[cols[0]] = cols[1].rstrip('\n')
	

	D_anvio_assembler= {}
	report_fileName = glob.glob('{0}/*_report_file.txt'.format(FS))[0]
	print report_fileName
	report_lines = open(report_fileName, 'r').readlines()
	for line in report_lines:
		cols = line.split('\t')
		name = cols[1].split(' ')[0]
		D_anvio_assembler[cols[0]] = name.rstrip('\n')
	

	D_anvio_JGI = {}
	for key in D_anvio_assembler.keys():
		D_anvio_JGI[key] = D_assembler_JGI[D_anvio_assembler[key]]
		
	return D_anvio_JGI


for FS in d_list:
	print FS
	map_fileName = glob.glob('{0}/*.a.map.txt'.format(FS))[0]
	print map_fileName
	map_lines = open(map_fileName, 'r').readlines()
	if map_lines[0].split('\t')[0][:2] == 'c_':
		D_anvio_JGI = shortcut(FS, map_lines)
	else:
		D_anvio_JGI = longway(FS, map_lines)
	
	print D_anvio_JGI[D_anvio_JGI.keys()[0]]
	print D_anvio_JGI[D_anvio_JGI.keys()[1]]
	
	outFile = open('{0}/{0}_contigs_anvio-JGI.pickle'.format(FS), 'wb')
	pickle.dump(D_anvio_JGI, outFile)
	outFile.close()
