# script that takes JGI-IMG output and formats it into a matrix to incorporate into anvi'o v.2.
#this is for the gene calls matrix. (anvi-gen-contigs-database)
# usage: python convert_jgi_orfs_to_anvi_matrix_ORFs_genome.py [jgi map file] [jgi .gff file]

import sys
import re

#first make a dictionary matching the original contig name to the IMG contig name
#NOTE!! when i put these into IMG the contig names had colons. when i formatted the contigs for anvi'o,
#i had to change the colons to underscores. this reflects that change.
D = {}
mapfile = open(sys.argv[1], 'r')
for l in mapfile:
	cs = l.split('\t')
	orig_name = cs[0]
	orig_name = orig_name.replace(':', '_')
	img_name = cs[1].rstrip('\n')
	D[img_name] = orig_name
mapfile.close()
#print D

#now make the ORF matrix
orf_file_handle = sys.argv[2]
outfile = open(orf_file_handle.replace('.gff', '_external_gene_calls_matrix.txt'), 'w')
outfile.write('gene_callers_id	contig	start	stop	direction	partial	source	version' + '\n')
orf_file = open(orf_file_handle, 'r')
for line in orf_file:
	cols = line.split('\t')
	if len(cols) > 1:
		contig_name = cols[0]
		id = cols[2]
		source = cols[1]
		start = int(cols[3]) -1 #because python indexes from 0
		stop = int(cols[4]) #because apparently meren counts differently from JGI and the last number is inclusive
		strand = cols[6]
		if strand == '+':
			direction = 'forward'
		if strand == '-':
			direction = 'reverse'
		if id == 'CDS':
			annotation = cols[8]
			#print annotation
			splits = annotation.split(';')
			id = splits[0].lstrip('ID=')
			annote = splits[2].rstrip('\n')
			annote = annote.replace('product=', '')
			#print annote
			outfile.write(str(id) + '\t'+ str(D[contig_name]) + '\t' + str(start) + '\t' + str(stop) + '\t' + str(direction) + '\t' + '0' + '\t' + str(source) + '\t' + str(source) + '\n')
		
orf_file.close()
outfile.close()
