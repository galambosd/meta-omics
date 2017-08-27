# script that takes JGI-IMG output and formats it into a matrix to incorporate into anvi'o v.2.
# this is for the functions matrix. (anvi-import-functions)
# usage: python convert_jgi_orfs_to_anvi_matrix_functions_genome.py [jgi .ko file]
#then later on you will do: anvi-import-functions -c contigs.db -i [the output of this script]
#if you want to use the pfam or tigerfam or cog files, you'll have to change this script to change the column numbers.


import sys
import re

#now make the ORF matrix
orf_file_handle = sys.argv[1]
outfile = open(orf_file_handle.replace('.ko.tab.txt', '_functions_matrix.txt'), 'w')
outfile.write('gene_callers_id	source	accession	function	e_value' + '\n')
orf_file = open(orf_file_handle, 'r')
for line in orf_file:
	cols = line.split('\t')
	id = cols[0]
	if id == 'gene_oid':
		pass
	else:
		ko = cols[9]
		annote = cols[10]
		evalue = cols[7]
		outfile.write(str(id) + '\t' + 'KO' + '\t' + str(ko) + '\t' + str(annote) + '\t' + str(evalue) + '\n')

orf_file.close()
outfile.close()