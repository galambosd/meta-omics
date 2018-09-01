# clustered heatmap of RNA expression of bins

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import argparse as ap
from numpy import arange
import scipy.cluster.hierarchy as hc
import scipy.spatial as sp
import scipy.stats.mstats as stats
from matplotlib.text import Text

# parser
parser = ap.ArgumentParser(description = 'A script to combine a clustered heatmap and a regular heatmap where the data share an axis.')
parser.add_argument('XL', metavar = 'CLUSTERED_EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table.")
parser.add_argument('XL2', metavar = 'DATA_EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table.")
parser.add_argument('-o', metavar = 'PLOT_FILE', default = False, help = 'Full file name for the *.pdf plot.')
parser.add_argument('-r', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered rows.')
parser.add_argument('-c', action = 'store_true', default = False, help = 'Make a heatmap with hierarchically clustered columns.')
parser.add_argument('--size', default = (6,27), nargs = 2, type = float, metavar = ('x','y'), help = 'Size of the regular heatmap. Default is (28,13).')


args = parser.parse_args()


# read the excel file
with pd.ExcelFile(args.XL) as xls:
    data = pd.read_excel(xls, 'normalized', index_col=0)
    alphabetical_bins = pd.Series(data.index)

with pd.ExcelFile(args.XL2) as xls:
    data2 = pd.read_excel(xls, 'table', index_col=0)

# samples = data.keys()[1:]

# can change figure size over here
#ax.set_yticklabels(bins, fontsize = 8)


fig = plt.figure(figsize = (args.size[0], args.size[1]))
ax = fig.add_subplot(1,1,1)

# plt.tight_layout(rect = [0.075,0,1,1])

cg = sb.clustermap(data, linewidths = 1.2, method = 'ward', metric = 'euclidean', figsize = (args.size[0], args.size[1]), z_score=0,linecolor='black',cmap = 'Blues',yticklabels = False, row_cluster=True, col_cluster=True)
row_index = cg.dendrogram_row.reordered_ind

#plt.tight_layout(rect = [0.075,0,1,1])
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize = 12)
plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize = 12)

# cg.ax_row_dendrogram.set_visible(False)

if not args.o:
    cg.savefig('combined_heatmap_clustered.pdf')
else:
    cg.savefig(args.o)


plt.cla()
plt.clf()



# data2['cluster_index'] = pd.Series(row_index,index=data2.index)
reordered_bins = alphabetical_bins.reindex(row_index)
data2 = data2.reindex(reordered_bins)
# data2=data2.drop(labels='cluster_index', axis='columns')

fig2 = plt.figure(figsize = (10, 13))
ax2 = fig2.add_subplot(1,1,1)
cg2 = sb.clustermap(data2, linewidths = 1.2, linecolor='black', cmap = 'Reds',figsize = (30, 27),method = 'ward', metric = 'euclidean', cbar = True, vmin = 0, vmax = 1, xticklabels = True, yticklabels = True, row_cluster = False, col_cluster = True)
plt.setp(cg2.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize = 12)
plt.setp(cg2.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize = 12)
if not args.o:
    cg2.savefig('heatmap_imposed_cluster_to_combine.pdf')
else:
    cg2.savefig('{}_2.pdf'.format(args.o.rstrip('.pdf')))
