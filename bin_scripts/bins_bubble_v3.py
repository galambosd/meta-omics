#!/usr/bin/env/python

import matplotlib.pyplot as plt
import pandas as pd
from numpy import arange, sqrt, power
from numpy.random import random
import argparse

parser = argparse.ArgumentParser(description = "This script takes the nearest 'calculations_for_bin_plots_v3.xlsx' " +
"file and makes a bubble plot of 15 archaeal bins across samples. The excel file should have a sheet called 'bin_bubble_plot'."+
" The genes and samples are hardcoded into the script.")


parser.add_argument('plot_type', metavar = 'PLOT_TYPE', choices = ['R', 'D', 'R:D'], help = "Choose either a [D]NA, [R]NA, or [R]NA[:][D]NA plot. "+
"This will influence the legend scale and which samples are included")

parser.add_argument('-o', metavar = 'output_file', help = "Choose a name for the *.pdf output file. Default is bins_bubble_plot_v3.pdf.")

args = parser.parse_args()

data=pd.read_excel("calculations_for_bin_plots_v3.xlsx", "bin_bubble_plot")

bins = []

#join bin columns to make full names with class and number
bins_pre = zip(data['Bin class'][:15], data['Bin number'][:15])

#add these w/ spaces included to bins list
for bin in bins_pre:
    bins.append(bin[0]+ ' #'+ bin[1].lstrip('Bin_'))


#Make a legend
#Works, but very ugly and obscures legend title
DNA_nums = [10, 100, 1000, 5000]
RNA_nums = [10, 100, 1000, 5000]
vs_nums = [power(1, 0.65)*70, power(10, 0.65)*70,
power(100, 0.65)*70, power(1000, 0.65)*70]
DNA_labels = ('5e-06','1e-06','1e-07','1e-08')
RNA_labels = ('5e-06','1e-06','1e-07','1e-08')
vs_labels = ('1000', '100', '10', '1')


# Make a samples list to use in the legend

if args.plot_type == 'R' or args.plot_type == 'R:D':
	samples = ['Hot Chimlet','Shrimp Canyon','Shrimp Gulley #2',
	'X-19 at BV #4','Ginger Castle','Hot Cracks #2',
	'Old Man Tree (2013)','Shrimp Hole (2012)', 'Shrimp Hole (2013)']
else:
	samples = ['Hot Chimlet','Shrimp Canyon','Shrimp Gulley #2',
	'X-19 at BV #4', 'Ginger Castle','Hot Cracks #2', 'Main Orifice',
	'near Main Orifice','Old Man Tree (2013)', 'Ravelin #2', 'Shrimp Buttery',
	'Shrimp Hole (2012)', 'Shrimp Hole (2013)', 'Twin Peaks']



fig = plt.figure(figsize=(7,10))

#Set number of xticks/yticks and remove frame
ax = fig.add_subplot(1,1,1, xticks = arange(1,len(samples)+1), yticks = arange(1,16), frame_on = False)

#set the ticklabels, font size, and orientation
ax.set_xticklabels(samples, fontsize = 5, ha = 'center', rotation = 90)
ax.set_yticklabels(bins, fontsize = 5, va ='center')


#Color code x-axis
#plt.axhline(y=-1,linewidth=4, color='r')

color_L = []

for color in data['color']:
    if color == 'r':
        color_L.append((1,0,0,0.14))
    else:
        color_L.append(color)

#Add outlines to bubbles and plot the data
# Third variable is size of the bubble, fifth creates black outlines
if args.plot_type == 'R:D':
    ax.scatter(data['x-axis'],data['y-axis (bins)'], s=data['size multiplier'], c=color_L, edgecolors = data['edge color'])
else:
    ax.scatter(data['x-axis'],data['y-axis (bins)'], s=data['size multiplier'], c=data['color'], edgecolors = 'k')

#plt.show()
plt.tight_layout(rect=[0.1,0.1,0.95,1]) #makes the layout match the dimensions and leaves room for text/caption/legend




axes = plt.gca()

#legend and legend sizes depend on RNA/DNA
if args.plot_type == 'R:D':
    nums = vs_nums
    labels = vs_labels
    y_lim = 0.2
    axes.set_xlim([0,10])
elif args.plot_type == 'D':
	nums = DNA_nums
	labels = DNA_labels
	y_lim = 0.6
else:
	nums = RNA_nums
	labels = RNA_labels
	y_lim = 0.0


#axes.set_xlim([0, len(samples)+1])

La = plt.scatter([], [], s=nums[0], color = 'w', edgecolor='k')
Lb = plt.scatter([], [], s=nums[1], color = 'w', edgecolor='k')
Lc = plt.scatter([], [], s=nums[2], color = 'w', edgecolor='k')
Ld = plt.scatter([], [], s=nums[3], color = 'w', edgecolor='k')


# FS854 = plt.scatter([], [], s = 200, color = 'g', edgecolor = 'k')
# FS844 = plt.scatter([], [], s = 200, color = 'b', edgecolor = 'k')
# FS856 = plt.scatter([], [], s = 200, color = 'm', edgecolor = 'k')
# FS881 = plt.scatter([], [], s = 200, color = 'r', edgecolor = 'k')

ax.legend((Ld,Lc,Lb,La), labels , scatterpoints = 1, loc = 'upper right', numpoints = 4, labelspacing = 3,
bbox_to_anchor=(0, 0), ncol = 1, fontsize = 8,
edgecolor = None, handletextpad = 6, frameon = False)

#Samples = ['Shrimp Hole (2012)\n(Von Damm)', 'X-19 at BV #4\n(Piccard)',
#'Shrimp Gulley #2\n(Piccard)', 'Old Man Tree (2013)\n(Von Damm)']


# ax.legend((FS854, FS844, FS856, FS881), Samples , scatterpoints = 1, loc = 'upper right', numpoints = 4, labelspacing = 2,
# bbox_to_anchor=(0, 0.03), ncol = 1, fontsize = 8,
# edgecolor = None, handletextpad = 6, frameon = False)

# Resize y axis and bring labels closer
axes.set_ylim([y_lim,len(bins)+1])
ax.tick_params(axis = 'x', which = 'major', pad = 5)

if args.o == None:
	plt.savefig('bins_bubble_plot_v3.pdf')
else:
	plt.savefig('{0}.pdf'.format(args.o))

#i am sure i could have spent more time fiddling with the colors, axis titles, etc but that's what illustrator is for
