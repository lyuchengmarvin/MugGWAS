This is the documentation on the functionality of this package and the prerequisite for the usage.

# Functionalities
MugGWAS identifies potential causal mutations for phenotypic change through testing associations between mutated genes and phenotypic values. 

Most GWAS tools classify variants into ref/alt before testing their association with the phenotype of interest. For example, an association between a single nucleotide variant and the phenotype is inferred if two variant groups significantly differ in the phenotypic value. However, a large genome, say 1 Gbp, requires a fairly large sample size to give enough power to test significance. Some tools test the presence/absence of genes to the phenotype. But, presence/absence does not capture the finer details of mutation. This tool will compile mutation signals of a gene and group variants into mutated versus unmutated genes, and test association like how presence/absence tools do.

**Future goals:**
- _2025.02.12_: We first focus on inferring mutation based on synonymous or nonsynonymous single nucleotide variants. We can work on integrating indels in the future.

# Prerequisites
This package uses the fixed effect model in  [`pyseer`](https://pyseer.readthedocs.io/en/master/index.html) for association analysis. So, the users have to install and match the [requirements](https://pyseer.readthedocs.io/en/master/installation.html#prerequisites) of `pyseer`.

This package also requires users to provide variant information on the tested genomes in vcf format. Implementing variant callers such as GATK HaplotypeCaller or FreeBayes can achieve this.

This package infers gene positions based on a single reference genome. Users should provide gene annotations for the reference, which can be acquired from annotation tools such as `bakta`.

# Installation
This is going to be a tool written in Python or pipelines assembled through Snakemake. Ideally, I want to have an easy installation process for the users. This involves two steps:

**Build environment**
Build an environment based on an `environment.yaml` file to satisfy software prerequisites and ensure applicability.
```
conda env create --name MugGWAS --file envs/environment.yaml
```

**Install package**
Install through conda
```
conda install muggwas
```

# Data format and requirements
MugGWAS test association between mutation and phenotype. It is recommended that the reference should be on the extreme end of the phenotypic spectrum.

- Input:
  - A `snp.vcf.gz` file: this should contain the variant information resulting from variant callers such as GATK HaplotypeCaller or FreeBayes. This should be in a vcf format and contain only single nucleotide variants. Users can extract snps by running this function `get_snp.py` in the scripts.
  - A `ref.gff` file: this should be the gene annotation of the reference genome, which contains information on the start and end positions for genes.
  - A gene presence and absence table: A tab-delimited file documenting the presence and absence of annotated genes in each assembly. This is an output from a roary run.
  - A phenotype file: a tab-delimited text file including the testing phenotype of interest. The rows of the table would be strain samples and the column is the phenotype. It can be either binary or continuous. The current version only supports one phenotype input at a time.
- Output:
  - Summary tables for the mutation types for each gene for each genome.
  - A table that categorizes genes into mutated or unmutated for the tested genomes.
  - A summary table of the statistical test results on each gene.

