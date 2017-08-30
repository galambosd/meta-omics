# script to get a list of protein clusters from a KO list

import argparse as ap

parser = ap.ArgumentParser(description = 'Supply an anvi-pan-genome summary file and a list of KOs to get a list of all protein clusters associated with those KOs.')

parser.add_argument('KO', type = ap.FileType('r'), help = 'A *.txt list of KOs.')
parser.add_argument('SUMMARY', type = ap.FileType('rb'), help = 'A binary file of the anvi-pan-genome summary.')
parser.add_argument('-o', metavar = 'OUTPUT_NAME', default = False, help = 'A name for the output file. Default is [KO filename]_PC.txt.')
args=parser.parse_args()

# Open the KO file
# Open summary file
# read the lines
# Close KO
# Close summary
with args.KO as f:
    KO_lines=f.readlines()
    KO_name = f.name
with args.SUMMARY as f:
    SUM_lines = f.readlines()

PC_list = []
# open outfile
if not args.o:
    outFile = open(KO_name.rstrip('.txt') + '_PC.txt', 'w')
else:
    outFile = open(args.o, 'w')
# for line in KO file...
for KO_line in KO_lines:
    # Get the KO number from the 1st column
    KO = KO_line.split('\t')[0]
    # for line in summary ...
    for line in SUM_lines:
        # split the lines
        cols = line.split('\t')
        # if the KO column = KO
        if KO in cols[5]:
            # add to list
            PC_list.append(cols[1]+'\n')

# write to outfile w/o duplicates:
for PC in set(PC_list):
    outFile.write(PC)

# close outfile
outFile.close()
