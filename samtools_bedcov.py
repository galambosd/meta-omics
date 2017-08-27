#!/usr/bin/env python

import glob, os, sys
from subprocess import call

assembly_S = os.getcwd()[-5:]

path = r'./'

logFile = open('{0}_samtools_log.txt'.format(assembly_S), 'w')

for bamName in glob.glob(os.path.join(path, '*_idba-init.bam')):
	print bamName
	bamName = bamName.lstrip('./')
	reads_S = bamName[:5]
	bedName = glob.glob('*.a.bed')[0]
	print bedName
	outFileName = '{0}_reads_vs_MidCaymanRise_{1}_idba_ORF_coverage.txt'.format(reads_S, assembly_S)
	run = 'samtools bedcov {0} {1} > {2}'.format(bedName, bamName, outFileName)
	print run
	logFile.write(run+'\n')
	code = call(run,shell = True)
	print 'Return code: {0}'.format(code)
	
	
for bamName in glob.glob(os.path.join(path, '*_idba_sorted.bam')):
	print bamName
	bamName = bamName.lstrip('./')
	reads_S = bamName[:5]
	bedName = glob.glob('*.a.bed')[0]
	print bedName
	outFileName = '{0}_RNA_reads_vs_MidCaymanRise_{1}_idba_ORF_coverage.txt'.format(reads_S, assembly_S)
	run = 'samtools bedcov {0} {1} > {2}'.format(bedName, bamName, outFileName)
	print run
	logFile.write(run+'\n')
	code = call(run,shell=True)
	print 'Return code: {0}'.format(code)
	
logFile.close()
