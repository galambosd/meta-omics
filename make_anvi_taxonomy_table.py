# makes a table to put into anvio using the "anvi-import-taxonomy" program based on the phylodist output.
# usage: python make_anvi_taxonomy_table.py [phylodist file]

import sys

#find infile
phylodist_file_handle = sys.argv[1]

#make outfile
outfile = open(phylodist_file_handle.replace('.txt', '_taxonomy_matrix.txt'),'w')
outfile.write('gene_callers_id	t_phylum	t_class	t_order	t_family	t_genus	t_species' + '\n')

#go through phylodist file line by line to make the anvio taxonomy file
infile = open(phylodist_file_handle, 'r')
for line in infile:
	cols = line.split('\t')
	idsplit = cols[0].split('_')
	id = idsplit[1]
	outfile.write(str(id))
	taxonomy = cols[4]
	tax_split = taxonomy.split(';')
	for x in tax_split[1:7]:	
		outfile.write('\t' + str(x))
	outfile.write('\n')

infile.close()
outfile.close()
	