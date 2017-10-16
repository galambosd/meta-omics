import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import argparse as ap
from numpy import arange
from matplotlib.text import Text

# parser
parser = ap.ArgumentParser(description = 'A script to make a binary heatmap out of a presence-absence table.')
parser.add_argument('XL', metavar = 'EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table and a sheet 'descriptions' with the descriptions.")
parser.add_argument('cols', metavar = 'BINS', type = int, help = 'Number of bins in excel file.')
parser.add_argument('-o', metavar = 'PLOT_FILE', default = False, help = 'Full file name for the *.pdf plot.')
parser.add_argument('-r', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered rows.')
parser.add_argument('-c', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered columns.')

args = parser.parse_args()


# which columns to read -- don't read first 2
cols = []
for x in arange(2, args.cols+2):
    cols.append(x)

# read the excel file
with pd.ExcelFile(args.XL) as xls:
    data = pd.read_excel(xls, 'table', index_col = 0, parse_cols = cols)
    descriptors = pd.read_excel(xls, 'descriptions')

genes = descriptors['Gene name']
bins = data.keys()[3:]

# can change figure size over here
fig = plt.figure(figsize = (7,13))
ax = fig.add_subplot(1,1,1)

#ax.set_yticklabels(bins, fontsize = 8)
ax.set_xticklabels(genes, fontsize = 8, rotation = 90)
sb.heatmap(data, cbar = False, vmin = 0, vmax = 1, ax = ax, xticklabels = True, yticklabels = True)
plt.tight_layout(rect = [0.075,0,1,1])
plt.yticks(rotation = 0, fontsize = 8)

if not args.o:
    plt.savefig('pan_binary_heatmap.pdf')
else:
    plt.savefig(args.o)

plt.clf()
plt.cla()

if args.c or args.r:
    fig2 = plt.figure(figsize=(7,17))
    ax2 = fig2.add_subplot(1,1,1)
    cg = sb.clustermap(data, figsize = (7,17),method = 'ward', metric = 'euclidean', cbar = False, vmin = 0, vmax = 1, xticklabels = True, yticklabels = True, row_cluster = args.r, col_cluster = args.c)
    #plt.tight_layout(rect = [0.075,0,1,1])
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize = 8)
    plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize = 8)

    if not args.o:
        cg.savefig('pan_binary_heatmap_clustered.pdf')
    else:
        cg.savefig(args.o.rstrip('.pdf')+'_clustered.pdf')
