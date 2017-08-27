#!/usr/bin/env python

# Run remove contigs < 1000 bp from gff, ko, phylodist files

import argparse, glob, pickle
from subprocess import call

parser = argparse.ArgumentParser(description = 'Remove contigs < 1000 bp long from all JGI-output KO, Gene Product' 
+'and Phylodist files. The script finds these files, plus a FASTA file, in directory names supplied by the user.')

parser.add_argument('-dir', metavar = 'DIRECTORY', default = False, help = 'A directory to look in. Works well w/ xargs.')

parser.add_argument('-list', metavar = 'LIST_FILE', type = argparse.FileType('rb'), 
	help = 'A Pickle-serialized list of directories to look in.')

args = parser.parse_args()
if args.dir == False:
	FS_list = pickle.load(args.list)
else:
	FS_list = []
	FS_list.append(args.dir)

for FS in FS_list:
	print FS
	print 'cd to {0}/'.format(FS)
	call('cd {0}/'.format(FS), shell = True)
	fasta_name = glob.glob('{0}/*.fa'.format(FS))[0]
	gff_name = glob.glob('{0}/*.a.gff'.format(FS))[0]
	gene_product_name = glob.glob('{0}/*.a.gene_product.txt'.format(FS))[0]
	KO_name = glob.glob('{0}/*.a.ko.txt'.format(FS))[0]
	phylo_name = glob.glob('{0}/*.a.phylodist.txt'.format(FS))[0]
	print '{0}\n{1}\n{2}\n{3}\n{4}'.format(fasta_name, gff_name, gene_product_name, KO_name, phylo_name)
	to_call1 = 'python ~/own_scripts/anvio_JGI_import/remove_contigs_smaller_than_1000bp_from_gff_gene_product_files_2.py {0} {1} {2}'.format(fasta_name, gff_name, gene_product_name)
	to_call2 = 'python ~/own_scripts/anvio_JGI_import/remove_contigs_smaller_than_1000bp_from_ko_files_only_2.py {0} {1}'.format(fasta_name, KO_name)
	to_call3 = 'python ~/own_scripts/anvio_JGI_import/remove_contigs_smaller_than_1000bp_from_phylodist_files_only_2.py {0} {1}'.format(fasta_name, phylo_name)
	print to_call1
	call(to_call1, shell = True)
	print to_call2
	call(to_call2, shell = True)
	print to_call3
	call(to_call3, shell = True)
	print 'cd ..'
	call('cd ..', shell = True)
	
	
