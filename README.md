# oligotyping_pipeline
A pipeline for oligotyping data analysis

## What does it do?
This pipeline expects an oligotyping directory. It will create an `oligotyping.sh`
shell script inside of the directory with all the commands to parse the input.

## Workflow

* Transpose the `MATRIX-COUNT.txt` and prepare it to become a biom formatted file
* Clean the representative node file, `NODE-REPRESENTATIVES.fasta` by removing the count data
* Align the representative nodes using QIIME's`align_seqs.py`
* Filter the alignment using QIIME's `filter_alignment.py`
* Make a phylogeny tree using QIIME's `make_phylogeny.py`
* Assign taxonomy using QIIME's `assign_taxonomy.py`
* Convert the transposed `MATRIX-COUNT.txt` to a JSON formatted biom
* Add the taxa assignments to the biom file
* If there is a sample mapping file, it will format that into a QIIME formatted mapping file

## Important output
* `oligotyping.sh`
    * List of commands to do the formatting
* `MATRIX-COUNT_TAXA.json`
    * The QIIME formatted biom file
* `tree.tree`
    The QIIME fomratted tree file

# Requirements
A python environment that has both `qiime` installed
