# script that takes JGI-IMG output and formats it into a matrix to incorporate into anvi'o v.2.
# this is for the functions matrix. (anvi-import-functions)
# usage: python convert_jgi_orfs_to_anvi_matrix_functions.py [jgi gene_product.txt file]
#then later on you will do: anvi-import-functions -c contigs.db -i [the output of this script]
#if you want to use the pfam or tigerfam or cog files, you'll have to change this script to change the column numbers.


import sys
import re

#now make the ORF matrix
orf_file_handle = sys.argv[1]
outfile = open(orf_file_handle.replace('.txt', '_functions_matrix.txt'), 'w')
outfile.write('gene_callers_id	source	accession	function	e_value' + '\n')
orf_file = open(orf_file_handle, 'r')
for line in orf_file:
	cols = line.split('\t')
	idsplit = cols[0].split('_')
	id = idsplit[1]
	if id == 'gene_oid':
		pass
	else:
		ko = cols[2].rstrip('\n')
		annote = cols[1]
		#evalue = cols[7]
		outfile.write(str(id) + '\t' + 'KO' + '\t' + str(ko) + '\t' + str(annote) + '\t' + '0' + '\n')

orf_file.close()
outfile.close()
