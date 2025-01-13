# MugGWAS
This repository stores code for the Mutated-gene Genome-Wide Association Study (MugGWAS).

Most GWAS tools classify variants into ref/alt before testing their association with the phenotype of interest. For example, an association between a single nucleotide variant and the phenotype is inferred if two variant groups significantly differ in the phenotypic value. However, a large genome, say 1 Gbp, requires a fairly large sample size to give enough power to test significance. Some tools test the presence/absence of genes to the phenotype. But, presence/absence does not capture the finer details of mutation. This tool will compile mutation signals of a gene and group variants into mutated versus unmutated gene, and test association like presence/absence.

- Input: a vcf file.
- Output: a summarized table of gene and mutations for each sample, a table that summarizes association test results.
