# This script uses KEGG_module_lex_parser to calculate the MCR for each
# MAG using a list of all the KOs present in the MAG.
# This is then plotted in a heatmap using seaborn/matplotlib.

import pandas as pd
import numpy as np
from sys import argv
from KEGG_module_lex_parser import *
import matplotlib.pyplot as plt
import seaborn as sb


# import modules file
modules = {}
with open(argv[1]) as module_file:
    module_file.readline()
    lines = module_file.readlines()
    for line in lines:
        split = line.split('\t')
        modules[split[1]] = split[2].rstrip('\n')

# import the bin KO description file
bin_KO = {}
with open(argv[2]) as bin_file:
    lines = bin_file.readlines()
    for line in lines:
        split = line.split('\t')
        bin_name = split[0]
        KOs = split[1].split(',')
        KO_list = []
        for KO in KOs:
            if ("Hypo" in KO) or ('COG' in KO) or ('pfam' in KO):
                continue
            for char in ['\'', ']', '[', ' ', '\n']:
                KO = KO.replace(char, '')
            KO_list.append(KO)
        bin_KO[bin_name] = KO_list


total = pd.DataFrame()
# for each module...
for module in modules.keys():
    mcr_list = []
    for bin in bin_KO:
        mcr = MCR(modules[module], bin_KO[bin])
        mcr_list.append(mcr)
    df = pd.DataFrame({module: mcr_list}, index=bin_KO.keys())
    total = pd.concat([total, df], axis=1)

total.to_csv('MCR_bins_across_pathways.txt', sep='\t', doublequote=False)
# for every bin in the bin_list, calculate the mcr and append to a list
# Make a series and then a dataframe, keep appending to the total dataframe

fig2 = plt.figure(figsize=(10, 13))
ax2 = fig2.add_subplot(1, 1, 1)
cg = sb.clustermap(total, linewidths=1, linecolor='black', cmap='Greens',
                   figsize=(30, 27), method='ward', metric='euclidean',
                   cbar=True, vmin=0, vmax=1, xticklabels=True,
                   yticklabels=True, row_cluster=True, col_cluster=True)

#plt.tight_layout(rect = [0.075,0,1,1])
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize=12)
plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=12)
# print it at the end into a tab-separated file

cg.savefig(argv[3])
