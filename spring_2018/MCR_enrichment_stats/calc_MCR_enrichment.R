# open the MCR dataset
args <- commandArgs(trailingOnly=TRUE)

total_mcr <- read.delim(file="MCR_bins_across_pathways.txt", quote='')
rownames(total_mcr) <- total_mcr$MAG
total_mcr<-subset(total_mcr, select = -c(MAG))
# define the list of modules to look at
mod_list <- read.delim(file=args[1], sep='\n', header=FALSE)
mod_list <- as.character(mod_list[,1])
# mod_list <- c("Cytochrome.bc1.complex.respiratory.unit","Thiosulfate.oxidation.by.SOX.complex..thiosulfate....sulfate","Glycolysis..Embden.Meyerhof.pathway...glucose....pyruvate","Dicarboxylate.hydroxybutyrate.cycle")

# define a list of bins as the "test" group. The rest are the control group
MAG_list <- read.delim(args[2], sep='\n', header=FALSE)
MAG_list <- as.character(MAG_list[,1])

x_group <- total_mcr[MAG_list,mod_list]
y_group <- total_mcr[setdiff(rownames(total_mcr),MAG_list), mod_list]

# open an outfile
# write the list of test bins


# create a dataframe for the results: module, control mean, test mean, MWW
i <- length(mod_list)
results <- data.frame('x mean' = numeric(i), 'y mean'=numeric(i), 'Method'=character(i), 'p-value'=numeric(i), stringsAsFactors=FALSE)
rownames(results) <- mod_list
# names(results) <- c('Module', 'x mean', 'y mean', 'stat method', 'p-value')

# for each module in the module list...
for (module in mod_list){
  # get average MCR of control and test
  x <- x_group[,module]
  y <- y_group[,module]
  x <- as.numeric(x)
  y <- as.numeric(y)
  x_mean <- mean(x)
  y_mean <- mean(y)

  # run a wilcox.test(x,y,alternative ="greater", correct=True) between two datasets
  wilcox <- wilcox.test(x,y,alternative ="t", correct=TRUE)
  # Doesn't assume normal dist, esp. small sample size
  # write the module name to file + the two averages, wilcox method, wilcox p-value result
  results[module,1] <- x_mean
  results[module,2] <- y_mean
  results[module,3] <- wilcox$method
  results[module,4] <- wilcox$p.value
}
write(names(total_mcr), file='abbreviated_module_names_R.txt')

write.table(results,file="MCR_enrichment.txt",row.names=TRUE,col.names=TRUE, quote=FALSE, sep='\t')
write('\nMAGs in group x:', file="MCR_enrichment.txt", append=TRUE)
write(MAG_list,file="MCR_enrichment.txt", sep = ',', append=TRUE)
