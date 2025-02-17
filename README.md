# MugGWAS
This repository stores code for the Mutated-gene Genome-Wide Association Study (MugGWAS).

## Rationale
Most GWAS tools classify variants into ref/alt before testing their association with the phenotype of interest. For example, an association between a single nucleotide variant and the phenotype is inferred if two variant groups significantly differ in the phenotypic value. However, a large genome, say 1 Gbp, requires a fairly large sample size to give enough power to test significance. Some tools test the presence/absence of genes to the phenotype. But, presence/absence does not capture the finer details of mutation. This tool will compile mutation signals of a gene and group variants into mutated versus unmutated genes, and test association like how presence/absence tools do.

## Data structure
The data should look like:
- Input:
  - A vcf file containing single nucleotide polymorphisms.
  - A gene presence and absence file for the tested genomes.
  - A gff file for the gene annotation of the reference genome.
  - A tab-delimited text file including the testing phenotype of interest.
- Output:
  - Summary tables for the mutation types for each gene for each genome.
  - A table that categorizes genes into mutated or unmutated for the tested genomes.
  - A summary table of the statistical test results on each gene.

## Flow Chart
In progress... Check [this link](https://app.diagrams.net/#G1-fR-q0M57sMw6OWWwv0d5StmVH5Il51p#%7B%22pageId%22%3A%22C5RBs43oDa-KdzZeNtuy%22%7D)...
