# clustered heatmap of RNA expression of bins

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import argparse as ap
from numpy import arange
from matplotlib.text import Text

# parser
parser = ap.ArgumentParser(description = 'A script to make a binary heatmap out of a presence-absence table.')
parser.add_argument('XL', metavar = 'EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table.")
parser.add_argument('cols', metavar = 'BINS', type = int, help = 'Number of bins to read from the Excel file.')
parser.add_argument('-o', metavar = 'PLOT_FILE', default = False, help = 'Full file name for the *.pdf plot.')
parser.add_argument('-r', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered rows.')
parser.add_argument('-c', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered columns.')
parser.add_argument('--size', default = (14,13), nargs = 2, type = float, metavar = ('x','y'), help = 'Size of the regular heatmap. Default is (14,13).')
parser.add_argument('--size_clustered', default = (13,13), type = float, nargs = 2, metavar = ('x','y'), help = 'Size of the clusterd heatmap. Default is (13,13).')


args = parser.parse_args()


# which columns to read -- don't read first 2
# cols = []
# for x in arange(1, (args.cols+2)):
#     cols.append(x)

# read the excel file
with pd.ExcelFile(args.XL) as xls:
    data = pd.read_excel(xls, 'normalized', index_col=0)

samples = data.keys()[1:]

# can change figure size over here
fig = plt.figure(figsize = (args.size[0], args.size[1]))
ax = fig.add_subplot(1,1,1)

#ax.set_yticklabels(bins, fontsize = 8)
ax.set_xticklabels(samples, fontsize = 12, rotation = 90)
sb.heatmap(data, ax = ax, cmap = 'Blues', linewidths = 1.2, linecolor='black',xticklabels = True, yticklabels = True)
plt.tight_layout(rect = [0.075,0,1,1])
plt.yticks(rotation = 0, fontsize = 12)

if not args.o:
    plt.savefig('bins_RNA_heatmap.pdf')
else:
    plt.savefig(args.o)

plt.clf()
plt.cla()

if args.c or args.r:
    fig2 = plt.figure(figsize=(10,13))
    ax2 = fig2.add_subplot(1,1,1)
    cg = sb.clustermap(data, linewidths = 1.2, linecolor='black',cmap = 'Blues',standard_scale=1, figsize = (args.size_clustered[0], args.size_clustered[1]),  method = 'ward', metric = 'euclidean', xticklabels = True, yticklabels = True, row_cluster = args.r, col_cluster = args.c)
    #plt.tight_layout(rect = [0.075,0,1,1])
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize = 12)
    plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize = 12)

    if not args.o:
        cg.savefig('bins_RNA_heatmap_clustered.pdf')
    else:
        cg.savefig(args.o.rstrip('.pdf')+'_clustered.pdf')
