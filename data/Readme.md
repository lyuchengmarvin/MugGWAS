This is a directory that stores tutorial datasets.

# Testing Dataset

To quickly implement this package's functions, a subset of data will be extracted from the pyseer dataset. This includes three resistant and three susceptible strains: 6925_1 #55, 7001_2 #12, 7553_5 #67, 6925_2 #76, 7553_5 #49, and 7622_5 #91. The small dataset can be found in the data directory.

The small dataset is extracted from the tutorial data through the script extract_small_data.py. 

```
python extract_small_data.py -p resistances.pheno -v snps.vcf.gz -sl 6925_1#55 7001_2#12 7553_5#67 6925_2#76 7553_5#49 7622_5#91
```

Aside from extracting the subset, the script also filters the vcf file based on these criteria:
- biallelic SNPs only
- removing SNPs with >= 5% of missing data
- removing SNPs with minor allele frequency <= 0.18

Before filtering, there were...
- Number of SNPs: 160672
- Number of SNPs with missing values over 5.0%: 0
- Number of SNPs with minor allele frequency smaller than 0.18: 145152

After filtering, there are...
- Number of SNPs: 15520
- Number of strains: 6

