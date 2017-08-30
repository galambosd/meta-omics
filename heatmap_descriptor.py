# get a list of PC and make a descriptor list of PC, KOs, their functions, and gene names

import argparse as ap

parser = ap.ArgumentParser(description = 'Provide a list of protein clusters and a the anvi-pan-genome summary file to get a summary of those clusters w/ KOs, gene names and functions')

parser.add_argument('PC_list', type = ap.FileType('r'), help = 'A *.txt list of protein cluster names.')
parser.add_argument('SUMMARY', type = ap.FileType('r'), help = 'A file of the anvi-pan-genome summary.')
parser.add_argument('KO', type = ap.FileType('r'), help = 'A *.txt list of KOs.')
parser.add_argument('-o', metavar = 'OUTPUT_NAME', default = False, help = 'A name for the output file. Default is [PC_filename]_short_summary.txt.')
args=parser.parse_args()

# open, read, close PC file
with args.PC_list as f:
    PC_lines = f.readlines()
    PC_name = f.name
# open, read, close Summary file
with args.SUMMARY as f:
    SUM_lines = f.readlines()
# open KO file
with args.KO as f:
    lines = f.readlines()
    KO_dict = {}
    # make dict of KO : tuple of gene name, function
    for line in lines:
        cols = line.split('\t')
        KO = cols[0]
        gene = cols[1].split('; ')[0]
        func = cols[1].split('; ')[1].rstrip('\n')
        KO_dict[KO] = (gene, func)


# open outfile
if not args.o:
    outFile = open(PC_name.rstrip('.txt') + '_short_summary.txt', 'w')
else:
    outFile = open(args.o, 'w')

# for line in PC_file...
for PC in PC_lines:
    PC = PC.rstrip('\n')
    # for line in summary...
    outFile.write(PC+'\t')
    KO_list = []
    gene_list = []
    func_list = []
    for line in SUM_lines:
        # split the line
        cols = line.split('\t')
        # if the PC column = PC:
        if cols[1] == PC.rstrip('\n'):
            # Add the KO to the KO_list
            KO = cols[5]
            if KO not in KO_list:
                KO_list.append(KO)
            if len(KO_list) > 1:
                more_KO = True
            # if the KO in that protein cluster isn't associated w/ methane, don't bother with the add't gene/functions annots
            if KO[-6:] not in KO_dict:
                continue
            gene = KO_dict[KO[-6:]][0]
            # get gene function and name from KO_dict, add to lists
            if gene not in gene_list:
                gene_list.append(gene)
            func = KO_dict[KO[-6:]][1]
            if func not in func_list:
                func_list.append(func)
    # join the KO, gene, func lists w/ '; ' and write them to outfile
    outFile.write('{0}\t{1}\t{2}\n'.format('; '.join(KO_list), '; '.join(gene_list), '; '.join(func_list)))


if more_KO:
    print 'Some protein clusters are associated with more than 1 KO!\a\a\a\a\a'
# close outfile
outFile.close()
