# script to prune a P-A table from an anvi-pan DB (table obtained w/ anvi-export-table)

import argparse as ap

parser = ap.ArgumentParser(description = 'Prune a presence-absence table to include only certain protein clusters. Takes a *.by P-A binary table and a *.txt list of protein cluster names [PC_*].')

parser.add_argument('t_file', metavar = 'TABLE', type = ap.FileType('rb'), help = 'Path to the presence-absence table binary file.')
parser.add_argument('pc_file', metavar = 'CLUSTERS', type = ap.FileType('r'), help = 'Path to the list of protein clusters to be included.')
parser.add_argument('-o', metavar = 'OUTFILE_NAME', default = False, help = 'Name to give to the new, pruned table.')
parser.add_argument('--make-both', action = 'store_true', default = False, help = 'Make both a binary and text output table. Default is text only.')

args = parser.parse_args()

# make a list out of the protein cluster file
#open a text outfile
#open a binary outfile if requested

# open the table
# write the first line of names to the outfile
# for every other line
    # split the line
    # if the 1st column (protein cluster) is in the pc list,
        # write the line to the outfile
        # if make-both:
            # binary too

# close everything up
