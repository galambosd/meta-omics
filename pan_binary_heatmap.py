import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import argparse as ap
from numpy import arange

parser = ap.ArgumentParser(description = 'A script to make a binary heatmap out of a presence-absence table.')
parser.add_argument('XL', metavar = 'EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table and a sheet 'descriptions' with the descriptions.")
parser.add_argument('-o', metavar = 'PLOT_FILE', default = False, help = 'Full file name for the *.pdf plot.')

cols = []
for x in arange(2, 72):
    cols.append(x)

args = parser.parse_args()
with pd.ExcelFile(args.XL) as xls:
    data = pd.read_excel(xls, 'table', parse_cols = cols)
    descriptors = pd.read_excel(xls, 'descriptions')

fig = plt.figure(figsize = (7,13))
ax = fig.add_subplot(1,1,1)
ax.set_xticklabels(data.keys(), fontsize = 8, rotation = 90)
ax.set_yticklabels(descriptors['Gene name'], fontsize = 8, rotation = 90, va = 'center')
sb.heatmap(data, cbar = False, vmin = 0, vmax = 1, ax = ax)


if not args.o:
    plt.savefig('pan_binary_heatmap.pdf')
else:
    plt.savefig(args.o)
