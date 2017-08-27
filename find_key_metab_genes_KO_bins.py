#goes through the KO annotations and finds key metabolism genes, and normalizes their abundances.

import sys, os, numpy, glob
path = r'./'

normalizationfile = open('normalization_factors.txt','r')
Dnorm = {}
for l in normalizationfile:
	cols = l.split('\t')
	metagenome = cols[0]
	normfactor = cols[1]
	Dnorm[metagenome] = normfactor
	
	
keygenesfile = open('key_metabolism_genes_KO.txt', 'r')
KOlist = []
Dgene = {}
Dannot = {}
Dmetab = {}
#i could have just iterated through this file rather than making a list and dictionaries... oh well.
for lin in keygenesfile:
	cs = lin.split('\t')
	KOnum = cs[0]
	KOlist.append(KOnum)
	gene = cs[1]
	Dgene[KOnum] = gene
	annot = cs[2]
	Dannot[KOnum] = annot
	metab = cs[3].rstrip('\n')
	Dmetab[KOnum] = metab
#print KOlist

for fileName in glob.glob(os.path.join(path, '*annotated_KO.txt')):
	print fileName
	fileName = fileName.lstrip('./')
	metagenomename_split = fileName.split('_reads_vs_')
	metagenomename = metagenomename_split[0]
	metagenomename = metagenomename[7:]
	outfilename = fileName.rstrip('.txt')
	outfile = open(str(outfilename) + '_key_metabolism_genes_normalized_KO.txt', 'w')
	outfile.write('KO Number	Gene	Annotation	Metabolism	Average coverage	Average coverage, normalized' + '\n')
	infile = open(fileName).read()
	for item in KOlist:
	#	print item
		covglist = []
		lines = infile.split('\n')
		for line in lines[:-1]:
			columns = line.split('\t')
			seqname = columns[0]
			database = columns[1].replace('KO:', '')
			#print database
			hitcount = columns[2].rstrip('\n')
			if database == item:
				covglist.append(float(hitcount))
				#print hitcounter
		average_hits = numpy.average(covglist)
		normalized_hits = average_hits / float(Dnorm[metagenomename])
		#print metagenomename
		#print item
		#print hitcounter
		#print normalized_hits
		outfile.write(str(item) + '\t' + str(Dgene[item]) + '\t' + str(Dannot[item]) + '\t' + str(Dmetab[item]) + '\t' + str(average_hits) + '\t' + str(normalized_hits) + '\n')

normalizationfile.close()
keygenesfile.close()
outfile.close()
	
