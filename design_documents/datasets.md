# Dataset structure

## Tutorial Datasets
This section describes a real dataset that will be used for testing the functionality in MugGWAS and a small subset of the data for fast testing.

_**Real dataset**_
This project will use the tutorial files used by the microbial GWAS tool – [Pyseer](https://pyseer.readthedocs.io/en/master/tutorial.html). The dataset can be downloaded from [here](https://figshare.com/articles/dataset/pyseer_tutorial/7588832?file=14091179), which includes the following files:

- `fsm_file_list.txt`: a list of strain names and their according genome names
- `assemblies.tar.bz2`: 616 *Streptococcus pneumoniae* genomes
- `resistances.pheno`: a tab-delimited text file containing strain names and their phenotypic value.
- `Spn23F.fa`: the genome assembly for the reference strain, [Spn23F](https://journals.asm.org/doi/10.1128/jb.01343-08).
- `Spn23F.gff`: the annotation file for `Spn23F.fa`
- `snps.vcf.gz`: a vcf file documenting single nucleotide polymorphisms (SNPs) mapped against the Spn23F reference genome.
- `gene_presence_absence.Rtab`: A tab-delimited file documenting the presence and absence of annotated genes in each assembly. This is an output from a roary run.

Croucher et al. (2015) collected and assembled the genomes. The raw sequence data can be found in the European Nucleotide Archive under the study name PRJEB2632. Phenotyping was done by measuring the minimum inhibitory concentrations for penicillin and ceftriaxone (Chewapreecha et al., 2014). Each strain was categorized as susceptible (0) and non-susceptible (1) according to their MIC values. Strains are considered susceptible when MIC values are smaller than 0.06 for penicillin and 0,5 for ceftriaxone.

_**Small dataset**_
To quickly implement this package's functions, a subset of data will be extracted from the _real dataset_. This includes three resistant and three susceptible strains: 6925_1 #55, 7001_2 #12, 7553_5 #67, 6925_2 #76, 7553_5 #49, and 7622_5 #91. The small dataset can be found in the `data` directory.

**Citations:**
- Lees, J.A., Galardini, M., Bentley, S.D. et al. Pyseer: a comprehensive tool for microbial pangenome-wide association studies. Bioinformatics 34(24): 4310–4312 (2018).
- Croucher, N., Finkelstein, J., Pelton, S. et al. Population genomic datasets describing the post-vaccine evolutionary epidemiology of Streptococcus pneumoniae. Sci Data 2, 150058 (2015).
- Chewapreecha, C., Marttinen, P., Croucher, N.J., et al.. Comprehensive identification of single nucleotide polymorphisms associated with beta-lactam resistance within pneumococcal mosaic genes. PLoS Genet, 10(8):e1004547 (2014).
