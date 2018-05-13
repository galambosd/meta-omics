library("optparse")
library("rPython")
library("heatmap3")
library('dplyr')

MCR<-function(module,bin){
  # pass these arguments to functions from the python file to
  result <- system(sprintf("python3 -c 'from KEGG_module_lex_parser import calc_MCR; print(calc_MCR('%s','%s'))'",module, bin), intern=T)
  # return the actual MCR number
 return(result)
}

option_list <- list(make_option(c("-m","--modules"),
  help="An ID, full name and KO definition for each of your modules.",
  metavar="modules"),make_option(c("-b","--bins"),
    help="Full names and KO contents for each bin.",
    metavar="bins"))

opt_parser=OptionParser(option_list=option_list)
args=parse_args(opt_parser)

# make a dictionary linking full module name and definitions

modules_df <-read.delim(args$modules)
module_defs <- modules_df[,3]
names(module_defs) <- modules_df[,2]

trim <- function(x){
 x <- gsub(" ","",x)
 x <- gsub("[[:punct:]]","",x)
 return(x)
}

# make a dictionary linking bins and KO content
bins_df <-read.delim(args$bins, header=FALSE)
bins_KO <- c()
i<-1
for (bin in bins_df[,2]){
  bins <- strsplit(bin, ',')
  bins <- lapply(bins, trim)
  bins_KO[[i]]<-bins
  i<-i+1
 }
names(bins_KO) <- bins_df[,1]


# create empty data frame for everything w/ as many rows as bins
output <- data.frame(names(bins_KO))

# rename the rows and columns
rownames(output)<-names(bins_KO)
names(output) <- c('BINS')

# for each module-bin combo, calculate MCR

for (module in names(module_defs)){
  col <- lapply(bins_KO, MCR, module = module_defs[[module]])
  names(col) <- module
  output <- left_join(output, col, by = 'BINS')
 }

 output <- subset(output, select = -c(output$BINS))

# put the number in a tab-delimited file w/ labeled rows/columns
write.table(output, file='bins_module_completetion.txt',row.names=TRUE,col.names=TRUE, quote=FALSE, sep='\t')
# if you want rows to be modules, put modules first in for loop

# go ahead and immediately plot a heatmap with clustering?
