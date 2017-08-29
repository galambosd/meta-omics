# script to prune a P-A table from an anvi-pan DB (table obtained w/ anvi-export-table)

import argparse as ap

parser = ap.ArgumentParser(description = 'Prune a presence-absence table to include only certain protein clusters. Takes a *.by P-A binary table and a *.txt list of protein cluster names [PC_*].')

parser.add_argument('t_file', metavar = 'TABLE', type = ap.FileType('rb'), help = 'Path to the presence-absence table binary file.')
parser.add_argument('pc_file', metavar = 'CLUSTERS', type = ap.FileType('r'), help = 'Path to the list of protein clusters to be included.')
parser.add_argument('-o', metavar = 'OUTFILE_NAME', default = False, help = 'Name to give to the new, pruned table.')
parser.add_argument('--make-both', action = 'store_true', default = False, help = 'Make both a binary and text output table. Default is text only.')

args = parser.parse_args()

# open the table
t_lines = args.t_file.readlines()
args.t_file.close()

# make a list out of the protein cluster file
pc_lines = args.pc_file.readlines()
clusters = []
for line in pc_lines:
    clusters.append(line.rstrip('\n'))
clusters = set(clusters)
args.pc_file.close()

#open a text outfile
if args.o == False:
    out_name = args.t_file.name
else:
    out_name = args.o
outFile = open(out_name, 'w')
#open a binary outfile if requested
if args.make-both:
    outFile2 = open(out_name, 'wb')

# write the first line of names to the outfile
outFile.write(t_lines[0])
if args.make-both:
    outFile2.write(t_lines[0])
# for every other line
for line in t_lines[1:]:
    # split the line
    cols = line.split('\t')
    # if the 1st column (protein cluster) is in the pc list,
    if cols[0] in clusters:
        # write the line to the outfile
        outFile.write(line)
        # if make-both:
        if args.make-both:
            outFile2.write(line)
            # binary too

# close everything up
outFile.close()
if make-both:
    outFile2.close()
