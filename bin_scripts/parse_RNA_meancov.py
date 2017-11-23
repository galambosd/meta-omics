#!/usr/bin/env python

from sys import argv
import os, glob
path = r'./'

FS_file = open('FS_list.txt', 'r')
FS_list = FS_file.readlines()

outfile = open('Bin_by_bin_mean_cov.txt', 'w')

for FS in FS_list:
	FS = FS.rstrip('\n')
	bin_file_name = '{}/bin_list.txt'.format(FS)
	bin_file = open(bin_file_name, 'r')
	bin_list = bin_file.readlines()
	outfile.write(FS+'\n')
	for bin in bin_list:
		bin = bin.rstrip('\n')
		cov_file_name = '{0}/{1}-mean_coverage.txt'.format(FS, bin)
		cov_lines = open(cov_file_name,'r').readlines()
		samples = cov_lines[0].split('\t')
		samples[-1]= samples[-1].rstrip('\n')
		vals = cov_lines[1].split('\t')
		vals[-1] = vals[-1].rstrip('\n')
		D = dict(zip(samples, vals))
		coverage = D['{0}_READS_VS_MIDCAYMANRISE_{0}_RNA_IDBA_SORTED'.format(FS)]
		print '{0}_READS_VS_MIDCAYMANRISE_{0}_RNA_IDBA_SORTED'.format(FS), coverage
		outfile.write(bin+'\t'+coverage+'\n')
	bin_file.close()
		
outfile.close()
FS_file.close()
		



