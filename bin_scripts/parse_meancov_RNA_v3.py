# parse anvi'o -mean_coverage.txt files to get mean coverage of bins. Then, normalize by # of RNA reads
# currently CANNOT do RNA and DNA at the same time
import argparse as ap
import os, glob

parser = ap.ArgumentParser(description='A script to get the normalized mean coverage of bins using anvi\'o *-mean_coverage.txt files.')
parser.add_argument('bin_list', metavar= 'BINS', help = 'A list of bins for which to calculate normalized mean coverage, samples included.')
# parser.add_argument('norms', metavar = 'NORMALIZATIONS', help = 'A list of normalization factors for all of the samples being analyzed.')
parser.add_argument('samples', metavar = 'SAMPLES', help = 'The list of samples where coverage is being calculated.')

args = parser.parse_args()

# open the normalization factors file and put it in a dictionary
#bin_samples = ['FS844','FS848','FS854','FS856','FS872','FS879','FS881']
# def readNormalizations(filePath):
#     norm_file = open(filePath, 'r')
#     normFactors ={}
#     lines = norm_file.readlines()
#     norm_file.close()
#     for line in lines:
#         cols = line.split('\t')
#         normFactors[cols[0]]= cols[1].rstrip('\n')
#     return normFactors

# All analyzed samples
def readSamples(filePath):
    sample_file = open(filePath,'r')
    samples = []
    lines = sample_file.readlines()
    sample_file.close()
    for line in lines:
        samples.append(line.rstrip('\n'))
    return samples

def getBins(filePath):
    to_read = {}
    new_name ={}
    inFile = open(filePath, 'r')
    line = inFile.readline()
    while True:
        print line
        current_sample = line.rstrip('\n').lstrip('!')
        line = inFile.readline()
        print line
        bins = []
        while '!' not in line:
            cols = line.split('\t')
            print cols
            if cols[0] == '':
                to_read[current_sample]=bins
                inFile.close()
                return to_read, new_name
            bin_name =cols[0]
            new_name[current_sample+'_'+bin_name]= cols[1].rstrip('\n')
            bins.append(bin_name)
            line = inFile.readline()
        to_read[current_sample]=bins


def copyAverages(outFile, binsDict, newNameDict):
    # for each key in the to_read dictionary
    print binsDict.keys()
    for key in binsDict.keys():
        # open the associated file
        curFile = open('{0}-mean_coverage.txt'.format(key), 'r')
        # read all the lines
        lines = curFile.readlines()
        # for line in lines:
        for line in lines:
            # split the columns, separate the 1st one
            cols = line.split('\t')
            # if the first column is in the bin_list...
            if cols[0] in binsDict[key]:
                # write the whole line to the output file, replacing bin name w/ new_name[bin]
                outFile.write(newNameDict[key+'_'+cols[0]])
                for item in cols[1:]:
                    outFile.write('\t'+item)
    # close the outFile
    outFile.close()

to_read, new_names = getBins(args.bin_list)
samples= readSamples(args.samples)

print to_read
print samples
print new_names

#open an output file and prep it with the right columns
outFile = open('bin_by_bin_meancov_excelPrep.txt', 'w')
outFile.write('Bin Name\t'+'\t'.join(samples)+'\n')

copyAverages(outFile, to_read, new_names)
print 'Done.'
