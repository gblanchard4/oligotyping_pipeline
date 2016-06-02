#!/usr/bin/env python
import argparse
from itertools import izip
import numpy as np

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
replace & transpose matrix
'''


def samples_to_otuid(line):
    return line.replace('samples\t', 'OTU ID\t')


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='replace & transpose matrix')

    # Input file
    parser.add_argument('-i', '--input', dest='input', help='The input file')
    # Output file
    parser.add_argument('-o', '--output', dest='output', help='The output file')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    outfile = args.output

    with open(infile, 'r') as inhandle, open(outfile, 'w') as outhandle:
        lines = inhandle.readlines()
        lines = [line.rstrip().split() for line in lines]
        lines[0][0] = lines[0][0].replace('samples', '#OTU ID')

        outhandle.write('\n'.join(['\t'.join(line) for line in list(np.array(lines).T)]))

if __name__ == '__main__':
    main()
