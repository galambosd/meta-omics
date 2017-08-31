import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import argparse as ap

parser = ap.ArgumentParser(description = 'A script to make a binary heatmap out of a presence-absence table.')
parser.add_argument('XL', metavar = 'EXCEL_FILE', help = "Excel file that has a sheet 'table' with the table and a sheet 'descriptions' with the descriptions.")
parser.add_argument('-o', metavar = 'PLOT_FILE', default = False, help = 'Full file name for the *.pdf plot.')

args = parser.parse_args()
with pd.ExcelFile(args.XL) as xls:
    data = pd.read_excel(xls, 'table', parse_cols = [2:])
    print data.keys()
    descriptors = pd.read_excel(xls, 'descriptions')

fig = plt.figure(figsize = (7,13))
ax = fig.add_subplot(1,1,1)

sb.heatmap(data, cbar = False, vmin = 0, vmax = 1, xticklabels = data.keys(), yticklabels = descriptors['Gene name'], ax = ax)


if not args.o:
    plt.savefig('pan_binary_heatmap.pdf')
else:
    plt.savefig(args.o)
