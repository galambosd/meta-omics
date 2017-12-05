# Quick redo of all_bins_taxonomy all_bins_taxonomy list

inFile = open('all_bins_taxonomy.txt', 'r')
outFile = open('all_bins_taxonomy_v2.txt','w')

lines = inFile.readlines()

for line in lines:
    bin_name = line.split('\t')[0]
    old_tax = lint.split('\t')[1].rstrip("\n")
    bin_number = bin_name.split('_')[-1]
    outFile.write(bin_name+'\t'+old_tax+'_'+bin_number+'\n')

inFile.close()
outFile.close()
