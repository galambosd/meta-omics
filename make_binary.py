# make a binary file from a text file
# v short

import argparse as ap

parser = ap.ArgumentParser(description = 'Save a binary copy of a txt file.')

parser.add_argument('file', metavar = 'FILE', type = ap.FileType('r'), help = 'Path to the text file to copy and save.')
parser.add_argument('-o', metavar = 'OUTFILE_NAME', default = False, help = 'Name to give to the *.bi outfile.')

args = parser.parse_args()

inFile = args.file
inLines = inFile.readlines()
inFile.close()

if args.o==False:
    outFile = open('{0}.bi'.format(inFile.name), 'wb')
else:
    outFile = open('{0}.bi'.format(args.o), 'wb')

for line in inLines:
    outFile.write(line)

outFile.close()
print 'Created a binary file {0}.'.format(outFile.name)
