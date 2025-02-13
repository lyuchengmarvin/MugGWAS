This is the documentation on the functionality of this package and the prerequisite for the usage.
# Functionalities

**Notes:**
- _2025.02.12_: We first focus on inferring mutation based on synonymous or nonsynonymous single nucleotide variants. We can work on integrating indels in the future.

# Prerequisites
This package uses the fixed effect model in  [`pyseer`](https://pyseer.readthedocs.io/en/master/index.html) for association analysis. So, the users have to install and match [the requirements of `pyseer`](https://pyseer.readthedocs.io/en/master/installation.html#prerequisites).

This package also requires users to provide variant information on the tested genomes in vcf format. Implementing variant callers such as GATK HaplotypeCaller or FreeBayes can achieve this.

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

- Input:
  - variant information: this is the result of variant callers such as GATK HaplotypeCaller or FreeBayes. This should be in a vcf format and contain only single nucleotide variants. Users can extract snps by running this function `get_snp.py` in the scripts.
  - Gene presence/absence file: this can be produced from pangenome analysis tools such as panaroo in the `.roary` format.
  - Gene position file: information on genes' start and end positions in gff format of the reference genome.
  - Phenotype: a tab-delimited text file including the testing phenotype of interest. The rows of the table would be strain samples and the column is the phenotype. It can be either binary or continuous. The current version only supports one phenotype input at a time.
- Output:
  - A summary table of mutated/unmutated genes for each sample. The rows would be gene names and the columns would be strain samples. This is essentially the gene presence/absence file, but it documents if genes are mutated.
  - A summary table of the statistical test results on each gene.

