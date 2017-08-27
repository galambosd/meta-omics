# Rika's script, slightly modified by David G

# this script removes all entries from contigs less than 1000bp from the JGI gff and ko files
# this is necessary if you have submitted a metagenome assembly that includes contigs smaller than 1000bp to JGI.
# anvi'o doesn't like it if your gene_product file has contigs that are missing from the contigs file.
# THIS SCRIPT ASSUMES THAT CONTIG NAMES ARE THE FIRST 18 CHARACTERS OF THE GENE NUMBER, AS PER JGI CONVENTION
# ie Ga0126447_100000156 is gene name, Ga0126447_1000001 is contig name
# usage: python remove_contigs_smaller_than_1000bp_from_gff_gene_product_files.py [fasta file] [gff file] [gene_product file] [map.txt file]

import sys, re, glob, pickle

print sys.argv[1][:5]
pickle_name = glob.glob('{0}/*_contigs_anvio-JGI.pickle'.format(sys.argv[1][:5]))[0]
print pickle_name
D_contig_names = pickle.load(open(pickle_name, 'rb'))



#change the FASTA_list to have JGI contig names, not anvio ones
#first, open the fasta file (with only 1000bp or above) and make a list of the fasta entries
fastalist = []
fastafile = open(sys.argv[1]).read()
fastas = fastafile.split('>')
for fasta in fastas[1:]:
	lines = fasta.split('\n')
	firstline = lines[0]
	JGI_name = D_contig_names[firstline.rstrip('\n')]
	fastalist.append(JGI_name)
#print fastalist
print 'Completed reading of fasta file. Contig name length is {0}'.format(len(fastalist[0])) 

#then use this list to fix the gff file
print 'Now working on new .gff file. This may take a while.'
gff_file_handle = sys.argv[2]
outfile_gff = open(gff_file_handle.replace('.gff','_contigs_over1kb.gff'), 'w')
gff_file = open(gff_file_handle, 'r')
for line in gff_file:
	cols = line.split('\t')
	contigname = cols[0]
	if contigname in fastalist:
		#print "match"
		outfile_gff.write(line)
gff_file.close()
outfile_gff.close()
print 'New .gff file done, called "..._contigs_over1kb.gff"'

#then use this list to fix the ko file
print 'Now working on new gene_product file'
gp_file_handle = sys.argv[3]
outfile_gp = open(gp_file_handle.replace('.gene_product.txt', '.gene_product_contigs_over1kb.txt'), 'w')
gp_file = open(gp_file_handle, 'r')
for l in gp_file:
	columns = l.split('\t')
	gene_name = columns[0]
	if gene_name[:len(fastalist[0])] in fastalist:
		outfile_gp.write(l)
gp_file.close()
outfile_gp.close()
print 'New gene_product file done, called "...gene_product_contigs_over1kb.txt"'
