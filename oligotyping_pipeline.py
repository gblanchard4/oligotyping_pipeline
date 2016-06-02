#!/usr/bin/env python
import argparse

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Run oligotyping and create a biom with taxonomic data
'''


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Run oligotyping and create a biom with taxonomic data')

    # Input file
    parser.add_argument('-i', '--input', dest='input', required=True, help='The input fasta')
    # Output file
    parser.add_argument('-o', '--output', dest='output', default='./oligotyping.sh', help='The output shell script')
    # Input file
    parser.add_argument('-m', '--map', dest='map', help='The metadata mapping file')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    outfile = args.output
    mapfile = args.map



    with open(outfile, 'w') as sh:
        # Decompose
        if mapfile:
            decompose_command = "decompose {} -E {}\n".format(infile, mapfile)
        else:
            decompose_command = "decompose {}\n".format(infile)
        sh.write(decompose_command)


if __name__ == '__main__':
    main()
