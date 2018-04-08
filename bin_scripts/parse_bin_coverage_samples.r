#!/usr/bin/env Rscript
library(optparse)
# a script to parse anvio files that show coverages of bins
# across samples and return an orderly excel/tsv file with normalized results

# set up arg parser
# list of sample files/bins that I want (formatted in some way to match bins to their samples)
# list of bin taxonomies to fix bin names
# normalization factors, tab-separated sample and number
# file w/ sample, sample name, all bins, comma-separated on each line

option_list <- list(make_option(c("-i","--bins_info"), type="character",
  help="A file describing samples, associated bins, and long bin names.",
  metavar="input"))

opt_parser=OptionParser(option_list=option_list)
args=parse_args(opt_parser)

# read in each file
sample_bin_info=read.delim(args.input)
# create a df
# stack it onto the existing df

# can you do dicts in R? If not, use a shell script where the below is w/ a shell script
# change all the column (sample) names to make more sense

# change all the rows (bin) names to make more sense

# divide each column by the normalization factor
