# script that takes JGI-IMG output and formats it into a matrix to incorporate into anvi'o v.2.
# you also have to give it the name of the anvio report file that comes from anvi-script-reformat-fasta
# this is for the gene calls matrix. (anvi-gen-contigs-database)
# usage: python convert_jgi_orfs_to_anvi_matrix_ORFs_metagenome.py [anvio_reformat_fasta_report_file] [jgi map file] [jgi .gff file]

import sys
import re
import pickle

D_file = open(sys.argv[4], 'rb')
D_anvio_JGI = pickle.load(D_file)
D = dict(zip(D_anvio_JGI.values(), D_anvio_JGI.keys()))


#now make the ORF matrix
orf_file_handle = sys.argv[3]
outfile = open(sys.argv[1].rstrip('_report_file.txt')+ '_external_gene_calls_matrix.txt', 'w')
outfile.write('gene_callers_id	contig	start	stop	direction	partial	source	version' + '\n')
orf_file = open(orf_file_handle, 'r')
for line in orf_file:
	#print line
	cols = line.split('\t')
	if len(cols) > 1:
		contig_name = cols[0]
		id = cols[2]
		source = cols[1]
		start = int(cols[3]) -1 #because python indexes from 0
		stop = int(cols[4]) #because apparently meren counts differently from JGI and the last number is inclusive
		strand = cols[6]
		#print strand
		if strand == '1':
			direction = 'f'
		if strand == '-1':
			direction = 'r'
		if id == 'CDS':
			annotation = cols[8]
			#print annotation
			splits = annotation.split(';')
			for split in splits:
				if 'locus_tag' in split:
					id = split.lstrip('locus_tag=')
					locustag_split = id.split('_')
					locus_tag = locustag_split[1]
			#id = splits[1].lstrip('locus_tag=')
			annote = splits[2].rstrip('\n')
			annote = annote.replace('product=', '')
			#print annote
			#print D[contig_name]
			outfile.write(str(locus_tag) + '\t'+ str(D[contig_name]) + '\t' + str(start) + '\t' + str(stop) + '\t' + str(direction) + '\t' + '0' + '\t' + str(source) + '\t' + str(source) + '\n')
		
orf_file.close()
outfile.close()
