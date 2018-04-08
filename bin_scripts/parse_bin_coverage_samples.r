#!/usr/bin/env Rscript
library(optparse)
# a script to parse anvio files that show coverages of bins
# across samples and return an orderly excel/tsv file with normalized results

# set up arg parser
# list of sample files/bins that I want (formatted in some way to match bins to their samples)
# list of bin taxonomies to fix bin names
# normalization factors, tab-separated sample and number
# file w/ sample, sample name, all bins, comma-separated on each line

option_list <- list(make_option(c("-i","--bins-info"), type="character",
  help="A file describing samples, associated bins, and long bin names.",
  metavar="input"),make_option(c("-s","--sample-names"), type="character",
    help="A file describing the long name for each sample.",
    metavar="longSNames"), make_option(c("-n","--norm-factors"), type="character",
    help="A file describing the normalization factor for each sample.",
    metavar="normFactors"))

opt_parser=OptionParser(option_list=option_list)
args=parse_args(opt_parser)

# create empty data frame for everything
total <- data.frame()

# read in each file
sample_bin_info <- read.delim(args.input)
binNames <- sample_bin_info[,2]
names(binNames) <- sample_bin_info[,1]

normFactorFrame <-read.delim(args.normFactors, header=FALSE)
normFactors <- normFactorFrame[,2]
names(normFactors) <- normFactorFrame[,1]

sNameFrame <- read.delim(args.longSNames, header=FALSE)
sNames <- sNameFrame[,2]
names(sNames)<- sNameFrame[,1]

nameBins <- function(x){
 return binNames[[x]]
}

nameSample <- function(x){
 return SNames[[x]]
}

# find each mean covg file
myFiles <- list.files(pattern="*mean_coverage.txt")
# for each one..
for (file in myFiles) {
  #open it
  current <- read.delim(file)
  #change the bin names
  sample <- substr(basename(file),1,5)
  current[,1] <- paste(current[,1], sample, sep="_")
  # stack it onto the existing df
  total <-rbind(total, current)
  # get rid of the weird indexing column that has indices from both DFs
  total <- subset(total, -total$X)
}


# change all the column (sample) names to make more sense
colNameList <- colnames(total)
colNames_short <- lapply(colNameList, nameSample)
colnames(total) <- colNames_short

# change all the rows (bin) names to make more sense
rowNameList <- rownames(total)
sample_bin_names <- paste(rowNameList, )
rowNames_short <- lapply(rowNameList, nameBins)
rownames(total) <- rowNames_short

# delete the bin names column
total <- subset(total, -total[,1])


# divide each column by the normalization factor
cols <- colnames(total)
for (col in cols) {
  total$col <- total$col / normFactors[[total$col]]
}

# write to an output text file
