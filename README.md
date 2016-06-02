# oligotyping_pipeline
A pipeline for oligotyping data analysis

## What does it do?
This pipeline expects a `fasta` file of your sequences and optionally a mapping
file. It will create an `oligotyping.sh` shell script that will put all output in
a folder titled **oligotyping_analysis/** at your current working directory.

## Workflow

* Run MED via the `decompose` command
* Transpose the `MATRIX-COUNT.txt` and prepare it to become a biom formatted file
* Clean the representative node file, `NODE-REPRESENTATIVES.fasta` by removing the count data
* Align the representative nodes using QIIME's`align_seqs.py`
* Filter the alignment using QIIME's `filter_alignment.py`
* Make a phylogeny tree using QIIME's `make_phylogeny.py`
* Assign taxonomy using QIIME's `assign_taxonomy.py`
* Convert the transposed `MATRIX-COUNT.txt` to a JSON formatted biom
* Add the taxa assignments to the biom file

## Important output
* `MATRIX-COUNT_TAXA.json`
    * A QIIME ready biom file
* `tree.tre`
    * A QIIME read tree file

# Requirements
A python environment that has both `oligotyping` & `qiime` installed
