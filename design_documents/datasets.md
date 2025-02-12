# Dataset structure

## Inputs & Outputs
The data should look like:
- Input:
  - Genotype: information of the genetic variants in a vcf format.
  - Gene presence/absence file: this can be produced from pangenome analysis tools such as panaroo in the `.roary` format.
  - Gene position file: information on genes' start and end positions in gff3 format of the reference genome.
  - Phenotype: a tab-delimited text file including the testing phenotype of interest. The rows of the table would be strain samples and the column is the phenotype. It can be either binary or continuous. The current version only supports one phenotype input at a time.
- Output:
  - A summary table of mutated/unmutated genes for each sample. The rows would be gene names and the columns would be strain samples. This is essentially the gene presence/absence file, but it documents if genes are mutated.
  - A summary table of the statistical test results on each gene.

## Tutorial Datasets
This project will use the tutorial files used by the microbial GWAS tool – [Pyseer](https://pyseer.readthedocs.io/en/master/tutorial.html). The dataset includes 616 *Streptococcus pneumoniae* genomes collected from Massachusetts (Croucher et al. 2015), a phenotype file documenting their resistance to *penicilin* and *ceftriaxone* (Chewapreecha et al. 2014), 

**Citations:**
- Lees, J.A., Galardini, M., Bentley, S.D. et al. Pyseer: a comprehensive tool for microbial pangenome-wide association studies. Bioinformatics 34(24): 4310–4312 (2018). https://doi.org/10.1093/bioinformatics/bty539
- Croucher, N., Finkelstein, J., Pelton, S. et al. Population genomic datasets describing the post-vaccine evolutionary epidemiology of Streptococcus pneumoniae. Sci Data 2, 150058 (2015). https://doi.org/10.1038/sdata.2015.58
- Chewapreecha C, Marttinen P, Croucher NJ, Salter SJ, Harris SR, Mather AE, Hanage WP, Goldblatt D, Nosten FH, Turner C, Turner P, Bentley SD, Parkhill J. Comprehensive identification of single nucleotide polymorphisms associated with beta-lactam resistance within pneumococcal mosaic genes. PLoS Genet. 2014 Aug 7;10(8):e1004547. doi: 10.1371/journal.pgen.1004547. PMID: 25101644; PMCID: PMC4125147.
