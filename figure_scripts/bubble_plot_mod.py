# Based on Rika's bubble_plot.py

import matplotlib.pyplot as plt
import pandas as pd
from numpy import arange
from numpy.random import random
from numpy import sqrt, power
import argparse

parser = argparse.ArgumentParser(description = "This script takes the nearest 'calculations for bubble_plots.xlsx' file and makes a "+
"bubble plot of the abudance/expression of key metabolic genes across metagenomic or metatranscriptomic samples. "+
"The excel file should have a sheet called 'MG_bubble_plot.' For formatting purposes, the genes and their order are hardcoded in the script.")

parser.add_argument('PLOT_TYPE', choices = ['D', 'R', 'R:D'], help = "Choose either a [D]NA, [R]NA, or [R]NA[:][D]NA plot. "+
"This will influence the legend scale and which samples are included")

parser.add_argument('-o', metavar = 'output_file', help = "Choose a name for the *.pdf output file. Default is MG_bubble_plot_modded.pdf.")

args = parser.parse_args()

font = 10.5

data=pd.read_excel("calculations_for_bubble_plots.xlsx", "MG_bubble_plot")

genes = ['sulfide:quinone oxidoreductase\n(sqr)', 'sulfur-oxidizing protein Sox\n(soxABCXYZ)',
'sulfate adenylyltransferase\n(sat, met3)', 'sulfite reductase\n(dsrAB)',
'2-oxoglutarate/\n2-oxoacid ferredoxin oxidoreductase\n(korABCD, oorABCD)',
'fumarate reductase\n(frdAB)', 'ATP-citrate lyase\n(aclAB)', 'carbon-monoxide dehydrogenase\n(cooCFS, acsA)',
'cytochrome c oxidase cbb3-type\n(ccoNOPQ_NO)', 'cytochrome c oxidase\n(coxABCD,AC, ctaF)',
'nitrite reductase (cytochrome c-552)\n(nrfA)', 'nitric oxide reductase\n(norB)',
'nitrite reductase (NO-forming)/\nhydroxylamine reductase (nirKS)', 'nitrous-oxide reductase\n(nosZ)',
'methyl-coenzyme M reductase\n(mcrABCDG)', 'methane/ammonia monooxygenase\n(pmoA-amoA)',
'[NiFe] hydrogenase\n(hydA2A3B2B3)', 'hydrogenase\n(hyaABC, hybO, hybC)',
'coenzyme F420 hydrogenase\n(frhABDG)','energy-converting hydrogenase B\n(ehbABFIJKLNO)',
'energy-converting hydrogenase A\n(ehaBCEGNOP)',
'ech hydrogenase\n(echABCE)', 'siderophore biosynthesis\n(IucA_IucC)',
'iron transport protein\n(FeoA)', 'iron transport protein\n(FeoB_C,N)',
'TonB-dependent Fe acquisition\n(Plug)', 'siderophore biosynthesis\n(Condensation)']

samples = []

#read samples
for num, sample in zip(data['y-axis (genes)'], data['Sample name']):
    if num == 2:
        break
    samples.append(sample)

fig = plt.figure(figsize=(8,15)) #i messed with the dimensions to make the plot taller
#Set number of xticks/yticks and remove frame
ax = fig.add_subplot(1,1,1, xticks = arange(1,len(samples)+1),
yticks = arange(1,len(genes)+1), frame_on = False)
#set the ticklabels, font size, and orientation
ax.set_xticklabels(samples, fontsize=12, rotation=90)
ax.set_yticklabels(genes, fontsize = 12, va ='center')


#Color code x-axis
#plt.axhline(y=-1,linewidth=4, color='r')

#Add outlines to bubbles and plot the data
# Third variable is size of the bubble, fifth creates black outlines
ax.scatter(data['x-axis (samples)'],data['y-axis (genes)'],
s=data['size multiplier'], c=data['color'], edgecolors = 'k')

#plt.show()
plt.tight_layout(rect=[0,0.065,0.95,1]) #makes the layout match the dimensions and
#leaves room for text/caption/legend

#Make a legend
#Works, but very ugly and obscures legend title
DNA_nums = [40, 400, 4000, 8000]
RNA_nums = [10,100,1000,5000]
vs_nums = [30,300, 3000, 6000]
DNA_labels = ('20','10','1','0.1')
RNA_labels = ('5e-04', '1e-04', '1e-05', '1e-06')
vs_labels = ('2e-03', '1e-03', '1e-04', '1e-05')

axes = plt.gca()

#legend and legend sizes depend on RNA/DNA
if args.PLOT_TYPE == 'R':
    nums = RNA_nums
    labels = RNA_labels
    y_lim = 0.1
    axes.set_xlim(left = -0.1)
elif args.PLOT_TYPE == 'D':
    nums = DNA_nums
    labels = DNA_labels
    y_lim = 0.6
    axes.set_xlim(left = -0.5)
else:
    nums = vs_nums
    labels = vs_labels
    y_lim = -0.05
    axes.set_xlim(left = -0.14)

La = plt.scatter([], [], s=nums[0], color = 'w', edgecolor='k')
Lb = plt.scatter([], [], s=nums[1], color = 'w', edgecolor='k')
Lc = plt.scatter([], [], s=nums[2], color = 'w', edgecolor='k')
Ld = plt.scatter([], [], s=nums[3], color = 'w', edgecolor='k')

ax.legend((Ld,Lc,Lb,La), labels , scatterpoints = 1,
loc = 'upper right', numpoints = 4, labelspacing = 3.5,
bbox_to_anchor=(0.05, -0.04), ncol = 1, fontsize = 8, handletextpad = 6, frameon = False)

# Resize y axis and bring labels closer
axes.set_ylim([y_lim,len(genes)+1])
ax.tick_params(axis = 'x', which = 'major', pad = 5)

if args.o == None:
	plt.savefig('MG_bubble_plot_modded.pdf')
else:
	plt.savefig('{0}.pdf'.format(args.o))

#i am sure i could have spent more time fiddling with the colors, axis titles, etc but that's what illustrator is for
