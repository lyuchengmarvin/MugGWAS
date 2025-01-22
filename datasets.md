# Dataset structure

## Inputs & Outputs
The data should look like:
- Input:
  - Genotype: information of the genetic variants in a vcf format.
  - Gene presence/absence file: this can be produced from pangenome analysis tools such as panaroo in the `.roary` format.
  - Gene position file: information of the start and end position of genes in a gff3 format.
  - Phenotype: a tab-delimited text file including the testing phenotype of interest. The rows of the table would be strain samples and the column is the phenotype. It can be either binary or continous. The current version only support one phenotype input at a time.
- Output:
  - A summary table of mutated/unmutated genes for each sample. The rows would be gene name and the columns would be strain samples. This is essentially the gene presence/absence file but documenting if genes are mutated or not instead of presence/absence.
  - A summary table of the statistical test results on each gene.

## Tutorial Datasets
Still looking...
