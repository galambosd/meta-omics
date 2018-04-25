library("optparse")
library("rPython")
library("heatmap3")

calc_MCR<-function(bins,modules){
  # pass these arguments to functions from the python file to
  # return the actual MCR number
 return()
}

option_list <- list(make_option(c("-m","--modules"),
  help="An ID, full name and KO definition for each of your modules.",
  metavar="modules"),make_option(c("-b","--bins"),
    help="Full names and KO contents for each bin.",
    metavar="bins"))

opt_parser=OptionParser(option_list=option_list)
args=parse_args(opt_parser)

# make a dictionary linking full module name and definitions

modules_df <-read.delim(args$modules, header=FALSE)
module_defs <- modules_df[,3]
names(module_defs) <- modules_df[,2]

# make a dictionary linking bins and KO content
bins_df <-read.delim(args$bins, header=FALSE)
bins_KO <- c()
i<-1
for (bin in bins_df[,2]:){
  bins_KO[[i]]<-strsplit(bin, ',')
  i<-i+1
 }
names(bins_KO) <- bins_KO[,1]


# create empty data frame for everything
output <- data.frame()

# rename the rows and columns
colnames(output)<-names(bins_KO)
rownames(output)<-names(module_defs)

# for each module-bin combo, calculate MCR

for (module in names(module):){
  for (bin in names(bins_KO):){
    output[module, bin]<-calc_MCR(module_defs[[module]], bins_KO[[bin]])
   }
 }

# put the number in a tab-delimited file w/ labeled rows/columns
write.table(output, file='bins_module_completetion.txt',row.names=TRUE,col.names=TRUE, quote=FALSE, sep='\t')
# if you want rows to be modules, put modules first in for loop

# go ahead and immediately plot a heatmap with clustering?
