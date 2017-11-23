import matplotlib.pyplot as plt
import pandas as pd
from numpy import arange
from numpy.random import random
from numpy import sqrt
import sys

data=pd.read_excel("calculations_for_bin_plots_v1.xlsx", "bin_bubble_plot")

bins = []

#join bin columns to make full names with class and number
bins_pre = zip(data['Bin class'], data['Bin number'])

#add these w/ spaces included to bins list
for bin in bins_pre:
	bins.append(bin[0]+ ' #'+ bin[1].lstrip('Bin_'))

# Make a samples list to use in the legend
samples = set(data['Sample name'])



fig = plt.figure(figsize=(7,13))

#Set number of xticks/yticks and remove frame
ax = fig.add_subplot(1,1,1, xticks = arange(1,1), yticks = arange(1,len(bins)+1), frame_on = False)

#set the ticklabels, font size, and orientation
ax.set_xticklabels([])
ax.set_yticklabels(bins, fontsize = 10, va ='center')


#Color code x-axis
#plt.axhline(y=-1,linewidth=4, color='r')

#Add outlines to bubbles and plot the data
# Third variable is size of the bubble, fifth creates black outlines
ax.scatter(data['x-axis'],data['y-axis (bins)'], s=data['size multiplier'], c=data['color'], edgecolors = 'k')

#plt.show()
plt.tight_layout(rect=[0.1,0.1,1,1]) #makes the layout match the dimensions and leaves room for text/caption/legend

#Make a legend
#Works, but very ugly and obscures legend title
#DNA_nums = [7.5, 75, 750, 3750]
vs_nums = [40, 400, 4000]
#DNA_labels = ('5','1','0.1','0.01')
vs_labels = ('100', '10', '1')


axes = plt.gca()

#legend and legend sizes depend on RNA/DNA
if 'v' in sys.argv[1]:
    nums = vs_nums
    labels = vs_labels
    y_lim = 0.2
    axes.set_xlim([0,2])
# else:
#     nums = DNA_nums
#     labels = DNA_labels
#     y_lim = 0.6

La = plt.scatter([], [], s=nums[0], color = 'w', edgecolor='k')
Lb = plt.scatter([], [], s=nums[1], color = 'w', edgecolor='k')
Lc = plt.scatter([], [], s=nums[2], color = 'w', edgecolor='k')
#Ld = plt.scatter([], [], s=nums[3], color = 'w', edgecolor='k')

Samples = ['Shrimp Hole (2012)\n(Von Damm)', 'X-19 at BV #4\n(Piccard)',
'Shrimp Gulley #2\n(Piccard)', 'Old Man Tree (2013)\n(Von Damm)']

FS854 = plt.scatter([], [], s = 200, color = 'g', edgecolor = 'k')
FS844 = plt.scatter([], [], s = 200, color = 'b', edgecolor = 'k')
FS856 = plt.scatter([], [], s = 200, color = 'm', edgecolor = 'k')
FS881 = plt.scatter([], [], s = 200, color = 'r', edgecolor = 'k')

ax.legend((Lc,Lb,La), labels , scatterpoints = 1, loc = 'upper right', numpoints = 3, labelspacing = 3.5,
bbox_to_anchor=(0, 0), ncol = 1, fontsize = 8,
edgecolor = None, handletextpad = 6, frameon = False)

ax.legend((FS854, FS844, FS856, FS881), Samples , scatterpoints = 1, loc = 'upper right', numpoints = 4, labelspacing = 2,
bbox_to_anchor=(0, 0.03), ncol = 1, fontsize = 8,
edgecolor = None, handletextpad = 6, frameon = False)

# Resize y axis and bring labels closer
axes.set_ylim([y_lim,len(bins)+1])
ax.tick_params(axis = 'x', which = 'major', pad = 5)

plt.savefig('bins_bubble_plot_v1.pdf')

#i am sure i could have spent more time fiddling with the colors, axis titles, etc but that's what illustrator is for
