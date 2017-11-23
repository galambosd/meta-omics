#!/usr/bin/env python

bin_file = open('Bin_by_bin_mean_cov.txt', 'r')
norm_file = open('normalization_factors_RNA.txt', 'r')

D_sample_norm = {}

for line in norm_file.readlines():
	cols = line.split('\t')
	name = cols[0].rstrip('_RNA')
	norm_factor = cols[1].rstrip('\n')
	D_sample_norm[name] = norm_factor

print "Normalized mean covg values for RNA:"
for line in bin_file.readlines():
	if 'FS' in line:
		sample_name = line.rstrip('\n')
		print sample_name
	else:
		cols = line.split('\t')
		bin = cols[0]
		covg = float(cols[1].rstrip('\n'))/float(D_sample_norm[sample_name])
		print bin + '\t' + str(covg)
		
bin_file.close()
norm_file.close()