#!/usr/bin/env python
# make an internal genome (bin) matrix for the anvi-gen-genomes command (prep for anvi-pan-genome)
# assumes a contigs db path of ~/pangenomics/<SAMPLE>/CONTIGS.db
# assumes a profile db path of ~/pangenomics/<SAMPLE>/profile/PROFILE.db
import argparse
# help, argparse, etc
parser = argparse.ArgumentParser(description = 'A script to make an internal genomes (bins) matrix for anvi-gen-genomes.')
message = """A TAB-delimited text file w/ columns [Sample name]\t[Bin ID]\t[Taxonomic class]"""
parser.add_argument('inFile', metavar = 'FILE', type = argparse.FileType('r'), help = message)
parser.add_argument('-o', metavar = 'OUTFILE_NAME', default = 'internal_genomes.txt', help = 'An optional name + path for the *.txt outfile.')
args = parser.parse_args()
# open tab delimited files that has samples and bin ids (from MCR excel files)
# read the infile
inLines = args.inFile.readlines()
# close the infile
args.inFile.close()
# open outfile
outFile = open(args.o, 'w')
# write the relevant column names
outFile.write('name\tbin_id\tcollection_id\tprofile_db_path\tcontigs_db_path\n')
# for line in infile
for line in inLines:
    cols = line.split('\t')
    # separate columns
    # write relevant data to outfile
    name = cols[2].rstrip('\n') + ' #' + cols[1].split('_')[1]
    if cols[0] == 'FS854':
        collection = 'FS854_bins_v232_refined'
    else:
        collection = '{0}_bins_v232'.format(cols[0])
    prof_path = '/Accounts/galambosd/pangenomics/{0}/profile/PROFILE.db'.format(cols[0])
    contig_path = 'Accounts/galambosd/pangenomics/{0}/CONTIGS.db'.format(cols[0])
    outFile.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(name, collection,prof_path, contig_path))
# close the outfile
outFile.close()
