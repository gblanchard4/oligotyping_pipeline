#!/usr/bin/env python
import argparse
import os

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
    # Input file
    parser.add_argument('-m', '--map', dest='map', help='The metadata mapping file')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    mapfile = args.map

    with open('oligotyping.sh', 'w') as sh:
        # Decompose
        if mapfile:
            decompose_command = "decompose {} -E {} -o oligotyping_analysis\n".format(infile, mapfile)
        else:
            decompose_command = "decompose {}\n".format(infile)
        sh.write(decompose_command)

        # Find the output folder
        oligotype_output_path = "oligotyping_analysis"

        matrix_count = "{}/MATRIX-COUNT.txt".format(oligotype_output_path)

        # Transpose MATRIX-COUNT
        otu_matrix = "{}/MATRIX-COUNT_T.txt".format(oligotype_output_path)
        replace_n_transpose_command = "replace_n_transpose.py -i {} -o {}\n".format(matrix_count, otu_matrix)
        sh.write(replace_n_transpose_command)

        # Clean Rep Set
        rep_set = "{}/NODE-REPRESENTATIVES.fasta".format(oligotype_output_path)
        rep_set_cleaned = "{}/NODE-REPRESENTATIVES.cleaned.fasta".format(oligotype_output_path)
        clean_repset_command = "clean_oligo_repset.py -i {} -o {}\n".format(rep_set, rep_set_cleaned)
        sh.write(clean_repset_command)

        # Align rep set
        align_repset_command = "align_seqs.py -i {} -o {}/pynast_aligned/\n".format(rep_set_cleaned, oligotype_output_path)
        sh.write(align_repset_command)
        # Filter alignment
        filter_alignment_command = "filter_alignment.py -i {0}/pynast_aligned/NODE-REPRESENTATIVES.cleaned_aligned.fasta -o {0}/pynast_aligned/\n".format(oligotype_output_path)
        sh.write(filter_alignment_command)
        # Make tree
        make_phylogeny_command = "make_phylogeny.py -i {0}/pynast_aligned/NODE-REPRESENTATIVES.cleaned_aligned_pfiltered.fasta -o {0}/tree.tre\n".format(oligotype_output_path)
        sh.write(make_phylogeny_command)

        # Assign Taxonomy
        assign_taxonomy_command = "assign_taxonomy.py -i {} -o {}/uclust_assigned_taxonomy\n".format(rep_set_cleaned, oligotype_output_path)
        sh.write(assign_taxonomy_command)
        taxa_assignments = "{}/uclust_assigned_taxonomy/NODE-REPRESENTATIVES.cleaned_tax_assignments.txt".format(oligotype_output_path)

        sh.write('biom convert -i {0}/MATRIX-COUNT_T.txt --to-json -o {0}/MATRIX-COUNT_T.json --table-type "OTU table"\n'.format(oligotype_output_path))
        sh.write('biom add-metadata -i {0}/MATRIX-COUNT_T.json -o {0}/MATRIX-COUNT_TAXA.json --observation-metadata-fp {1} --observation-header OTUID,taxonomy,confidence,method --sc-separated taxonomy\n'.format(oligotype_output_path, taxa_assignments))


if __name__ == '__main__':
    main()
