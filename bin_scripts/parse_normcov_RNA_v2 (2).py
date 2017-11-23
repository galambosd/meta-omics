#!/usr/bin/env python
 
from sys import argv
import os, glob
path = r'./'

# make a dict of FS# to its sample name and make a separate ordered list of just the sample names
def get_sample_names(name):
    D_sample_names = {}
    FS_list = []
    # this tab-delimited text file has matches of FS to sample name
    sample_names = open(name, 'r')
    lines = sample_names.readlines()
    sample_names.close()
    # read it in and return the dictionary
    for line in lines:
        cols = line.split('\t')
        D_sample_names[cols[0]] = cols[1].rstrip('\n')
        FS_list.append(cols[0])
    return D_sample_names, FS_list

D_sample_names, FS_list = get_sample_names('sample_names_archaea.txt')

# list of all sites in Piccard
L_sites_PD = ['FS851', 'FS852','FS854', 'FS856']


# build dict connecting bin number to taxonomy
D_taxa = {}

tax_file = open('bin_taxonomy.txt')
for line in tax_file.readlines():
	cols = line.split('\t')
	D_taxa[cols[0]] = [cols[1], cols[2].rstrip('\n')]

# list of sample sites in archaea
# FS_file = open('../FS_list.txt', 'r')
# FS_list = FS_file.readlines()

# open the normalization factors
norm_file = open('normalization_factors_RNA.txt', 'r')
 
# make a dict connecting normalization factors to sample name
D_sample_norm = {}
 
for line in norm_file.readlines():
    cols = line.split('\t')
    name = cols[0].rstrip('_RNA')
    norm_factor = cols[1].rstrip('\n')
    D_sample_norm[name] = norm_factor 
 

outfile = open('bin_by_bin_normalized_cov.txt', 'w')
 
for FS in FS_list:
    FS = FS.rstrip('\n')
    
    # get a list of the bins in that FS to know which ones to open later
    bin_file_name = '{}/bin_list.txt'.format(FS)
    bin_file = open(bin_file_name, 'r')
    bin_list = bin_file.readlines()
   
    for bin in bin_list:
        bin = bin.rstrip('\n')
        #open, format, read covg file for each bin
        # go into the directory of the current FS, go bin by bin
        cov_file_name = '{0}/{1}-mean_coverage.txt'.format(FS, bin)
        cov_lines = open(cov_file_name,'r').readlines()
        samples = cov_lines[0].split('\t')
        samples[-1]= samples[-1].rstrip('\n')
	samples = samples [1:]
        vals = cov_lines[1].split('\t')
    	vals[-1] = vals[-1].rstrip('\n')
	vals = vals[1:]
        
        # for each mapping, meancov value pair in the bin's meancov file...
        for sample, val in zip(samples, vals):
        	# get normalized coverage by dividing the mean coverage from the file by the # of RNA reads in that mapping
        	sample_name = sample[0:5]
		norm_cov = str(float(val) /  float(D_sample_norm[sample[0:5]]))
        	
        	print '{0}/{1}'.format(bin, sample[0:5])
        	
        	# the first 5 characters of the mapping name are the FS name 
		if bin == 'Bin_13' and sample_name == 'FS848':
			bin_tax = 'Euryarchaea'
			bin_class = 'Methanococci'
        	else:
        		bin_tax = D_taxa[bin][0]
        		bin_class = D_taxa[bin][1]
        	site = sample_name in L_sites_PD
        	outfile.write(norm_cov + '\t' + D_sample_names[sample_name] + '\t' + bin_tax + '\t' + bin_class + '\t' + bin + '\t' + str(site) + '\n')
    bin_file.close()
         
outfile.close()
tax_file.close()
norm_file.close()
