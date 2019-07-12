# This script uses anvio files to make a simply-formatted
# list of the KOs in each MAG

from sys import argv


# create a dictionary mapping MAG abbreviations to full names
MAG_name_dict = {}
with open(argv[1]) as binFile:
    lines = binFile.readlines()
    for line in lines:
        splits = line.split('\t')
        MAG = splits[0]
        full_name = splits[1].rstrip('\n')
        MAG_name_dict[MAG] = full_name

outFile = open('bin_KO_definitions.txt', 'w')

MAG_KO_dict = {}

# Using the anvio gene calls file for each MAG, build a dictionary mapping
# MAG name to a KEGG module list
for MAG in MAG_name_dict:
    splits = MAG.split('_', maxsplit=1)
    shortMAG = splits[1]
    sample = splits[0]
    # this path is hard-coded right now.
    with open('SUMMARY_{0}_bins_RNA/bin_by_bin/{1}/{1}-gene_calls.txt'.
              format(sample, shortMAG)) as binKOFile:
        binKOFile.readline()
        lines = binKOFile.readlines()
        KO_list = []
        for line in lines:
            splits = line.split('\t')
            KO_row = splits[6].split(',')
            for KO in KO_row:
                KO = KO.lstrip('KO:')
                KO = 'K' + KO
                KO_list.append(KO)
        MAG_KO_dict[MAG] = KO_list

for MAG in MAG_KO_dict:
    outFile.write(MAG_name_dict[MAG] + '\t' + str(MAG_KO_dict[MAG]) + '\n')

outFile.close()
