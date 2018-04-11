#!/usr/bin/env Rscript --vanilla
library("optparse")
# a script to parse anvio files that show coverages of bins
# across samples and return an orderly excel/tsv file with normalized results

# set up arg parser
# list of sample files/bins that I want (formatted in some way to match bins to their samples)
# list of bin taxonomies to fix bin names
# normalization factors, tab-separated sample and number
# file w/ sample, sample name, all bins, comma-separated on each line

option_list <- list(make_option(c("-i","--bins_info"),
  help="A file describing samples, associated bins, and long bin names.",
  metavar="input"),make_option(c("-s","--sample_names"),
    help="A file describing the long name for each sample.",
    metavar="longSNames"), make_option(c("-n","--norm_factors"),
    help="A file describing the normalization factor for each sample.",
    metavar="normFactors"))

opt_parser=OptionParser(option_list=option_list)
args=parse_args(opt_parser)

# create empty data frame for everything
total <- data.frame()

# read in each file
sample_bin_info <- read.delim(args$bins_info, header=FALSE)
binNames <- sample_bin_info[,2]
names(binNames) <- sample_bin_info[,1]

normFactorFrame <-read.delim(args$norm_factors, header=FALSE)
normFactors <- normFactorFrame[,2]
names(normFactors) <- normFactorFrame[,1]

sNameFrame <- read.delim(args$sample_names, header=FALSE)
sNames <- sNameFrame[,2]
names(sNames)<- sNameFrame[,1]

nameBins<-function(x){
 return(binNames[[x]])
}

nameSample <- function(x){
 return(sNames[[x]])
}



# find each mean covg file
myFiles <- list.files(pattern="*mean_coverage.txt")
# for each one..
for (file in myFiles) {
  #open it
  print(file)
  current <- read.delim(file)
  sample <- substr(basename(file),1,5)
  #standardize the bin names
  current$bins <- paste(sample, current$bins, sep="_")
  print(current)
  # take out the bins that aren't complete
  current <- subset(current, current$bins %in% names(binNames))
  # rename the rows to standardized bin names
  rownames(current) <- current$bins
  # take out the bins column
  current <- subset(current, select=-bins)

  # standardize the sample names
  colnames(current) <- substr(colnames(current),1,5)

  # normalize everything so far
  for (i in c(1:ncol(current))) {
    current[,i] <- current[,i]/normFactors[i]
  # stack it onto the existing df
  }
  print(current)
  print(length(rownames(current)))
  # get rid of the weird indexing column that has indices from both DFs
  #total <- subset(total, -total$X)
  total <-rbind(total, current)
  print(total)
  print(length(rownames(total)))

}

# # change all the column (sample) names to make more sense
# colNameList <- colnames(total)
# colNames_short <- substr(colNameList,1,5)
# colnames(total) <- binNames[[colNames_short]]
#
#
# # change all the rows (bin) names to make more sense
# rowNameList <- rownames(total)
# rownames(total) <- binNames[[rowNameList]]
#
#
# # delete the bin names column
# total <- subset(total, -total$bins)
#
#
# # divide each column by the normalization factor

colnames(total) <- sapply(colnames(total), nameSample)
rownames(total) <- sapply(rownames(total), nameBins)


# write to an output text file
print("Done. Saved normalized coverages to 'normalized_covg_bins_RNA.txt'")
write.table(total,file="normalized_covg_bins_RNA.txt",row.names=TRUE,col.names=TRUE, quote=FALSE, sep='\t')
