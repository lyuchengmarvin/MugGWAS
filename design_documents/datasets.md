## Tutorial Datasets
This section describes a real dataset that will be used for testing the functionality of MugGWAS.

**Real dataset**
This project will use the tutorial files used by the microbial GWAS tool – [Pyseer](https://pyseer.readthedocs.io/en/master/tutorial.html). The dataset can be downloaded from [here](https://figshare.com/articles/dataset/pyseer_tutorial/7588832?file=14091179), which includes the following files:

- [ ] `fsm_file_list.txt`: a list of strain names and their according genome names.
- [ ] `assemblies.tar.bz2`: 616 *Streptococcus pneumoniae* genomes.
- [X] `resistances.pheno`: a tab-delimited text file containing strain names and their phenotypic value.
- [X] `Spn23F.fa`: the genome assembly for the reference strain, [Spn23F](https://journals.asm.org/doi/10.1128/jb.01343-08).
- [X] `Spn23F.gff3`: the annotation file for `Spn23F.fa`. This is downloaded from [NCBI](https://www.ncbi.nlm.nih.gov/nuccore/NC_011900.1) since what they provided is in a wrong format.
- [X] `snps.newname.vcf.gz`: a vcf file documenting single nucleotide polymorphisms (SNPs) mapped against the Spn23F reference genome.
- [ ] `gene_presence_absence.Rtab`: A tab-delimited file documenting the presence and absence of annotated genes in each assembly. This is an output from a roary run.
_** The checked files are required for MugGWAS.**_

Croucher et al. (2015) collected and assembled the genomes. The raw sequence data can be found in the European Nucleotide Archive under the study name PRJEB2632. Phenotyping was done by measuring the minimum inhibitory concentrations for penicillin and ceftriaxone (Chewapreecha et al., 2014). Each strain was categorized as susceptible (0) and non-susceptible (1) according to their MIC values. Strains are considered susceptible when MIC values are smaller than 0.06 for penicillin and 0,5 for ceftriaxone.

**Biological significance**
Understanding the genetic basis of a trait is central to many biological research that help gain mechanismtic insight into complex biological phenomena. For instance, the discovery of genetic loci that contribute to antibiotic resistance better our knowledge for how important pathogens evolve to escape medicinal application. While most tools associate traits with raw genetic variants, most variants do not result in functional change at the gene level. MugGWAS provides a new angle at inferring the genetic basis for a microbial trait by associating gene mutation to trait variation. Through the annotation of disruptive mutation types such as nonsense, missense, stopgain or nonstop, MugGWAS identifies the putative dysfunction of a gene associated with phenotypic change.

**Small dataset**
To quickly implement this package's functions, a subset of data will be extracted from the _real dataset_. This includes 150 resistant and 150 susceptible strains specified in the tab-delimited file-"selected_samples.txt". The small dataset can be found in the `data` directory.

```
python extract_small_data.py \
  -p resistances.pheno \
  -v snps.newname.vcf.gz \
  -s selected_samples.txt
```

The small dataset is extracted from the tutorial data through the script `extract_small_data.py`.
Aside from extracting the subset, the script also filters the vcf file based on these criteria:
- biallelic SNPs only
- removing SNPs with >= 5% of missing data
- removing SNPs with minor allele frequency <= 0.01 to allow for rare variants (important for small datasets).

Before filtering, there were...
- Number of SNPs: 160,672
- Number of SNPs with missing values over 5.0%: 0
- Number of SNPs with minor allele frequency smaller than 0.01: 74,089
After filtering, there are...
- Number of SNPs: 91,717
- Number of strains: 300

**Citations:**
- Lees, J.A., Galardini, M., Bentley, S.D. et al. Pyseer: a comprehensive tool for microbial pangenome-wide association studies. Bioinformatics 34(24): 4310–4312 (2018).
- Croucher, N., Finkelstein, J., Pelton, S. et al. Population genomic datasets describing the post-vaccine evolutionary epidemiology of Streptococcus pneumoniae. Sci Data 2, 150058 (2015).
- Chewapreecha, C., Marttinen, P., Croucher, N.J., et al.. Comprehensive identification of single nucleotide polymorphisms associated with beta-lactam resistance within pneumococcal mosaic genes. PLoS Genet, 10(8):e1004547 (2014).
