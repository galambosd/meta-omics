#goes through the KO annotations and finds key metabolism genes, and normalizes their abundances.
#this is just a check to look at iron genes, which i will add to the analysis.

import sys, os, numpy, glob
path = r'./'

normalizationfile = open('normalization_factors.txt','r')
Dnorm = {}
for l in normalizationfile:
	cols = l.split('\t')
	metagenome = cols[0]
	normfactor = cols[1]
	Dnorm[metagenome] = normfactor
	
	
keygenesfile = open('pfam_genes.txt', 'r')
KOlist = []
Dgene = {}
Dannot = {}
#Dmetab = {}
#i could have just iterated through this file rather than making a list and dictionaries... oh well.
for lin in keygenesfile:
	cs = lin.split('\t')
	KOnum = cs[1].rstrip('\n')
	KOlist.append(KOnum)
	gene = cs[0]
	Dgene[KOnum] = gene.rstrip('\n')
	#annot = cs[2]
	#Dannot[KOnum] = annot
	#metab = cs[3].rstrip('\n')
	#Dmetab[KOnum] = metab
#print KOlist

for fileName in glob.glob(os.path.join(path, '*annotated_pfam.txt')):
	print fileName
	fileName = fileName.lstrip('./')
	metagenomename_split = fileName.split('_reads_vs_')
	metagenomename = metagenomename_split[0]
	metagenomename = metagenomename[7:]
	outfilename = fileName.rstrip('.txt')
	outfile = open(str(outfilename) + '_key_metabolism_genes_normalized_pfam.txt', 'w')
	outfile.write('Pfam Number	Gene	Annotation	Metabolism	Number of raw hits	Normalized hits' + '\n')
	infile = open(fileName).read()
	for item in KOlist:
	#	print item
		covlist = []
		lines = infile.split('\n')
		for line in lines[:-1]:
			columns = line.split('\t')
			seqname = columns[0]
			database = columns[1]
			#print database
			hitcount = columns[2].rstrip('\n')
			if database == item:
				covlist.append(float(hitcount))
				#print hitcounter
		average_covg = numpy.average(covlist)
		normalized_hits = float(average_covg) / float(Dnorm[metagenomename])
		#print metagenomename
		#print item
		#print hitcounter
		#print normalized_hits
		outfile.write(str(item) + '\t' + str(Dgene[item]) + '\t' + 'iron' + '\t' + 'iron' + '\t' + str(average_covg) + '\t' + str(normalized_hits) + '\n')

normalizationfile.close()
keygenesfile.close()
outfile.close()
	
