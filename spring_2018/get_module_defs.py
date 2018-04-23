#!/usr/bin/env python3
import requests
import argparse as ap

parser = ap.ArgumentParser(description = "A script using the KEGG API to download module definitions for a list of modules.")
parser.add_argument('M_list', help = "A .txt file with the list of KEGG modules as M#####.")

args = parser.parse_args()

# open the list of modules
inFile = open(args.M_list)

modules = []

for line in inFile.readlines():
    line = line.rstrip('\n')
    modules.append(line)
# get rid of any possible duplicates
modules = set(modules)


outFile = open('module_definitions.txt','w')
outFile.write('Module number\tModule name\tKO definition\n')

# for each of our modules, download our data
for m in modules:
    r = requests.get("http://rest.kegg.jp/get/md:{}".format(m))
    if r.status_code != 200: # 200 is the success code
        print("The online request for {} encountered an error".format(m))
    # after getting the data, parse the module name and definition from it
    m_data = r.text
    # split the data into lines
    m_data_lines = m_data.split('\n')
    # get the second half of the 2nd line
    m_name = m_data_lines[1].split(maxsplit=1)[1]
    #get the 2nd half of the 3rd line
    m_def = m_data_lines[2].split(maxsplit=1)[1]
    outFile.write(m+'\t'+m_name+'\t'+m_def+'\n')

outFile.close()
print('Done.')
