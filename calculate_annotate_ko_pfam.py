#!/usr/bin/env python

import glob, os
from subprocess import call

path = r'./'
for fileName in glob.glob(os.path.join(path, '*_ORF_coverage.txt')):
	print fileName
	fileName = fileName.lstrip('./')
	koName = glob.glob('*.a.ko.txt')[0]
	pfamName = glob.glob('*.a.pfam.txt')[0]
	print koName
	print pfamName
	run1 = 'python ~/bubble_plots/scripts_for_bubble_plots/calculate_gene_coverage_annotate_ko.py {0} {1}'.format(fileName, koName)
	run2=  'python ~/bubble_plots/scripts_for_bubble_plots/calculate_gene_coverage_annotate_pfam.py {0} {1}'.format(fileName, pfamName)
	print run1
	print run2
	code1 = call(run1, shell = True)
	code2 = call(run2, shell = True)
	print 'Return codes: {0}, {1}'.format(code1, code2)
