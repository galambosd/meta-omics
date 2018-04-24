#!/usr/bin/env python

def calculate_MCR(module, bin):
    pass

def main(arg):
    import argparse as ap

    parser = ap.ArgumentParser(description='A script that takes KEGG module definitions'+
        'a list of KOs for each bin and calculates MCR.')
    parser.add_argument('-m', '--modules', metavar='modules', help='An ID, full name and KO definition for each of your modules.')
    parser.add_argument('-b','--bins', metavar='bins', help='Full names and KO contents for each bin.')

    args = parser.parse_args()
    print(args)

    # make a dictionary linking full module name and definitions

    # make a dictionary linking bins and KO content

    # make an outfile

    # for each module-bin combo, calculate MCR

    # put the number in a tab-delimited file w/ labeled rows/columns

if __name__ == '__main__':
    main()
