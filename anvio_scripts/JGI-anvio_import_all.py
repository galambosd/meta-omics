# Make all external gene call matrices, create contig dbs w/ external gene calls
# AND run hmms, create functions matrix, import functions matrix, create taxonomy matrix, import taxonomy

import argparse, glob, pickle
from subprocess import call

parser = argparse.ArgumentParser(description = 'Script to import external JGI gene calls, functions, and taxonomy into a new anvio contigs database.')

parser.add_argument('-dir', metavar = 'DIRECTORY', default = False, help = 'A directory to look in. Works well w/ xargs.')

parser.add_argument('-list', metavar = 'LIST_FILE', type = argparse.FileType('rb'), help = 'A Pickle-serialized list of directories to look in.')

args = parser.parse_args()
if args.dir == False:
	FS_list = pickle.load(args.list)
else:
	FS_list = []
	FS_list.append(args.dir)


def find(search):
	result =  glob.glob(search)[0]
	print 'Found {0}'.format(result)
	return result

def run_script(to_call):
	print to_call
	call(to_call, shell = True)

#for each sample in the imported pickle list...
for FS in FS_list:
	print 'cd {0}'.format(FS)
	call('cd {0}/'.format(FS), shell = True)
	#Get anvi-reformat report name
	report_name = find('{0}/{0}_report_file.txt'.format(FS))
	#Get jgi map name
	map_name = find('{0}/*.a.map.txt'.format(FS))
	#Get gff name (NEW)
	gff_name = find('{0}/*.a_contigs_over1kb.gff'.format(FS))
	#Create gene calls matrix
	run_script('python /Accounts/galambosd/own_scripts/anvio_JGI_import/convert_jgi_orfs_to_anvi_matrix_ORFs_metagenome_2.py {0} {1} {2} {3}/{3}_contigs_anvio-JGI.pickle'.format(report_name, map_name, gff_name, FS))
	
	#Get name of external gene calls matrix
	gene_calls = find('{0}/*_external_gene_calls_matrix.txt'.format(FS))
	#Get fasta name
	fasta = find('{0}/MidCaymanRise_{0}_idba_assembly_fixed.fa'.format(FS))
	#Run anvi-gen-contigs-db
	run_script('anvi-gen-contigs-database -f {0} --split-length -1 --external-gene-calls {1} --ignore-internal-stop-codons -o {2}/CONTIGS.db'.format(fasta, gene_calls, FS))
	
	#Run HMMs on DB
	contigs_db = find('{0}/*.db'.format(FS))
	run_script('anvi-run-hmms -c {0} -T 60'.format(contigs_db))
	
	#Find gene products file (NEW)
	gene_product = find('{0}/*.a.gene_product_contigs_over1kb.txt'.format(FS))
	#Create functions matrix
	run_script('python /Accounts/galambosd/own_scripts/anvio_JGI_import/convert_jgi_orfs_to_anvi_matrix_functions_metagenome.py {0}'.format(gene_product))
	
	#Find functions matrix name
	functions = find('{0}/*_functions_matrix.txt'.format(FS))
	#Import functions into contigs DB
	run_script('anvi-import-functions -c {0} -i {1}'.format(contigs_db, functions))
	
	#Find phylodist file (NEW)
	phylodist = find('{0}/*.a.phylodist_contigs_over1kb.txt'.format(FS))
	#Create taxonomy matrix
	run_script('python /Accounts/galambosd/own_scripts/anvio_JGI_import/make_anvi_taxonomy_table.py {0}'.format(phylodist))
	
	#Find taxonomy matrix
	taxonomy = find('{0}/*_taxonomy_matrix.txt'.format(FS))
	#Import taxonomy to contigs DB
	run_script('anvi-import-taxonomy -c {0} -i {1} -p default_matrix'.format(contigs_db, taxonomy))
	
	print FS + ' done.'
	print 'cd ..'
	call('cd ..', shell = True)
	
	
print 'Done.'
