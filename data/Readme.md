This is a directory that stores tutorial datasets.

# Testing Dataset

To quickly implement this package's functions, a subset of data will be extracted from the example dataset. This includes four resistant and four susceptible strains: ND_86,ND_102,ND_85,ND_79,ND_100,ND_98,ND_101,ND_90. The small dataset can be found in the data directory.

The small dataset is extracted from the tutorial data through the script extract_small_data.py. 

```
python extract_small_data.py -p grazing_defense_trait.txt -v graz_LE.snp.vcf -sl ND_86 ND_102 ND_85 ND_79 ND_100 ND_98 ND_101 ND_90
```

Aside from extracting the subset, the script also filters the vcf file based on these criteria:
- biallelic SNPs only
- removing SNPs with >= 5% of missing data
- removing SNPs with minor allele frequency <= 0.18

Before filtering, there were...
- Number of SNPs: 21154
- Number of strains: 8
- Number of SNPs with missing values over 5.0%: 0
- Number of SNPs with minor allele frequency smaller than 0.18: 15082

After filtering, there are...
- Number of SNPs: 6072
- Number of strains: 8

