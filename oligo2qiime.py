#!/usr/bin/env python
import argparse
import os

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Prepare Oligotyping Data for QIIME
'''


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Prepare Oligotyping Data for QIIME')

    # Input Dir
    parser.add_argument('-i', '--input', dest='input', required=True, help='The input oligotyping directory')

    # Parse arguments
    args = parser.parse_args()
    indir = os.path.abspath(args.input)

    shell_script = '{}/prepare_oligotyping.sh'.format(indir)
    with open(shell_script, 'w') as sh:

        # Find the output folder
        oligotype_output_path = indir

        # Make a directory to keep our finalized files
        sh.write("mkdir {}/QIIME_Ready\n".format(oligotype_output_path))

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
        make_phylogeny_command = "make_phylogeny.py -i {0}/pynast_aligned/NODE-REPRESENTATIVES.cleaned_aligned_pfiltered.fasta -o {0}/QIIME_Ready/tree.tre\n".format(oligotype_output_path)
        sh.write(make_phylogeny_command)

        # Assign Taxonomy
        assign_taxonomy_command = "assign_taxonomy.py -i {} -o {}/uclust_assigned_taxonomy\n".format(rep_set_cleaned, oligotype_output_path)
        sh.write(assign_taxonomy_command)
        taxa_assignments = "{}/uclust_assigned_taxonomy/NODE-REPRESENTATIVES.cleaned_tax_assignments.txt".format(oligotype_output_path)

        # Transpose MATRIX-COUNT
        matrix_count = "{}/MATRIX-COUNT.txt".format(oligotype_output_path)
        otu_matrix = "{}/MATRIX-COUNT_T.txt".format(oligotype_output_path)
        replace_n_transpose_command = "replace_n_transpose.py -i {} -o {}\n".format(matrix_count, otu_matrix)
        sh.write(replace_n_transpose_command)
        # Format BIOM
        sh.write('biom convert -i {0}/MATRIX-COUNT_T.txt --to-json -o {0}/MATRIX-COUNT_T.json --table-type "OTU table"\n'.format(oligotype_output_path))
        sh.write('biom add-metadata -i {0}/MATRIX-COUNT_T.json -o {0}/MATRIX-COUNT_TAXA.json --observation-metadata-fp {1} --observation-header OTUID,taxonomy,confidence,method --sc-separated taxonomy\n'.format(oligotype_output_path, taxa_assignments))

        # Noderize biom
        biom = "{}/MATRIX-COUNT_TAXA.json".format(oligotype_output_path)
        noderized = "{}/QIIME_Ready/otus.biom".format(oligotype_output_path)
        sh.write('noderize_med_biom.py -i {} -o {}\n'.format(biom, noderized))

        # Clean map... maybe
        map_file = '{}/SAMPLE-MAPPING.txt'.format(oligotype_output_path)
        if os.path.isfile(map_file):
            map_file_cleaned = '{}/map.clean.txt'.format(oligotype_output_path)
            sh.write('clean_oligo_map.py -i map_file -o {}\n'.format(map_file_cleaned))

        med_params = "summarize_taxa:level 1,2,3,4,5,6,7,8\nplot_taxa_summary:labels Kingdom,Phylum,Class,Order,Family,Genus,Species,Node\n \
                        alpha_diversity:metrics shannon,simpson,PD_whole_tree,chao1,observed_species\nmultiple_rarefactions:min 100\n \
                        multiple_rarefactions:max NNN\nmultiple_rarefactions:step NNN\nbeta_diversity_through_plots:seqs_per_sample NNN\n"
        sh.write('echo "{}" > {}/QIIME_Ready/params.txt'.format(med_params, oligotype_output_path))
if __name__ == '__main__':
    main()
