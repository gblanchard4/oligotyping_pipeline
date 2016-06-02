#!/usr/bin/env python
import argparse

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Clean Oligotyping Rep Set file
'''


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Cleans up the counts from an Oligotyping rep set')

    # Input file
    parser.add_argument('-i', '--input', dest='input', help='The input file')
    # Output file
    parser.add_argument('-o', '--output', dest='output', help='The output file')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    outfile = args.output

    with open(infile, 'r') as inhandle, open(outfile, 'w') as outhandle:
        for line in inhandle:
            if line.startswith('>'):
                line = "{}\n".format(line.split('|')[0])
                outhandle.write(line)
            else:
                outhandle.write(line)

if __name__ == '__main__':
    main()
