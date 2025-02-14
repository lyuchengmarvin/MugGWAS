# This script extracts a subset of data from the tutorial data set
# Author: Yu-Cheng Lin
# Time: 2025-02-13

import os
import argparse
import pysam
import subprocess
from collections import Counter

# Extract specific strains from the phenotypic data
def extract_phenotypic_data(input_file, strains):
    '''
    This function extracts specific strains from the phenotypic data and output to a new file.
    
    strains: a list of strains to extract
    input_file: a tab-delimited file in which first column is strain names and the second column is phenotypic data.
    output_file: a tab-delimited file that contains the extracted strains.
    '''
    output_prefix = input_file.split('.')[0]
    output_file = f"{output_prefix}.subset.txt"
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as out:
            header = f.readline()
            out.write(header)
            for line in f:
                strain = line.split('\t')[0]
                if strain in strains:
                    out.write(line)

# Run bcftools to extract snps from a vcf file
def bcftool_extract_snp(input_vcf, output_vcf, strains):
    '''
    This function extracts snps from a vcf file using bcftools.

    strains: a list of strains to extract
    input_vcf: a vcf file that contains snp data.
    '''
    command = f"export PATH=/Users/linyusheng/bcftools_1.9/bin/:$PATH && bcftools view -v snps -m2 -M2 -s {','.join(strains)} {input_vcf} -o {output_vcf} -O z"
    print("Making sure vcf contains only biallelic SNPs...")
    print("Running bcftools with command:", command)
    subprocess.run(command, shell=True)
    print(f"SNP extraction completed. Output file: {output_vcf}")

# Calculate minor allele frequency
def calculate_maf(allele_counts):
    total_alleles = sum(allele_counts.values())
    if total_alleles == 0:
        return 0.0
    # Exclude None or any invalid keys
    valid_alleles = {allele: count for allele, count in allele_counts.items() if allele is not None}
    if len(valid_alleles) <= 1:
        return 0.0
    # Calculate frequencies and determine MAF
    frequencies = {allele: count / total_alleles for allele, count in valid_alleles.items()}
    minor_allele_freq = min(frequencies.values())
    return minor_allele_freq

# Filter vcf file based on the number of missing values and minor allele frequency
def filter_snp_data(input_snp_vcf, output_vcf, missing_threshold=0.95, maf_threshold=0.18):
    '''
    This function filters the snp data based on the number of missing values and minor allele frequency
    '''
    # Open the input and output files
    vcf_in = pysam.VariantFile(input_snp_vcf)
    vcf_out = pysam.VariantFile(output_vcf, 'w', header=vcf_in.header)
    # counter for missing data and maf
    num_missing = 0
    num_maf_fail = 0

    print(f"Filtering SNPs based on missing data proportion >= {missing_threshold} and MAF <= {maf_threshold}...")

    for record in vcf_in:
        total_samples = len(record.samples)
        
        # Count missing genotypes
        missing_count = sum(1 for sample in record.samples.values() if sample['GT'] is None or all(allele is None for allele in sample['GT']))
        
        # Calculate missing data proportion
        missing_proportion = missing_count / total_samples

        # Count how many snps fail the filtering threshold
        if missing_proportion >= missing_threshold:
            num_missing += 1
            
        # Count alleles
        allele_counts = Counter()
        for sample in record.samples.values():
            gt = sample['GT']
            if gt is not None:
                allele_counts.update(gt)

        # Calculate MAF
        maf = calculate_maf(allele_counts)
        # Count how many snps fail the filtering threshold
        if maf <= maf_threshold:
            num_maf_fail += 1

        # Filter based on missing data and MAF, either one fails the threshold will be filtered out
        if missing_proportion <= missing_threshold and maf >= maf_threshold:
            vcf_out.write(record)

    # Report statistics
    print("")
    print(f"Number of SNPs with missing values over {100-missing_threshold * 100}%: {num_missing}")
    print(f"Number of SNPs with minor allele frequency smaller than {maf_threshold}: {num_maf_fail}")
    print("")
    # Close the files
    vcf_in.close()
    vcf_out.close()
    print(f"Filtered SNPs written to {output_vcf}")

# Read the extracted snp data and report the number of snps and strains
def report_snp_data_statistics(input_snp_vcf):
    '''
    This function reads the extracted snp data and make summary statistics.
    The statistics report should include the number of snps and strains, the number of snps with missing values over 5%, and the number of snps with minor allele frequency smaller than 0.18.
    
    input_snp_vcf: a vcf file that contains snp data.
    '''
    num_snps = 0
    num_strains = 0
    
    with pysam.VariantFile(input_snp_vcf) as vcf:
        for record in vcf:
            num_snps += 1
            num_strains = len(record.samples)
    print("")
    print(f"Number of SNPs: {num_snps}")
    print(f"Number of strains: {num_strains}")
    print("")


# Main function
def main():
    """
    input_pheno: a tab-delimited file that contains phenotypic data
    input_vcf: a vcf file that contains genetic variant data
    """
    parser = argparse.ArgumentParser(description="Extract a subset of data from the tutorial data set.")
    parser.add_argument("-p","--phenotypic_data", type=str, help="Input tab-delimited phenotypic data file")
    parser.add_argument("-v","--genetic_variant_data", type=str, help="Input vcf data file")
    parser.add_argument("-sl","--strains", nargs='+', help="List of strains to extract")
    args = parser.parse_args()

    phenotype_file = os.path.join(os.getcwd(), 'pyseer_dataset/',args.phenotypic_data)
    vcf_file = os.path.join(os.getcwd(), 'pyseer_dataset/', args.genetic_variant_data)
    strains = list(args.strains)


    # Run bcftools to extract snps from a vcf file
    output_prefix = vcf_file.split('/')[-1].split('.')[0]
    extract_file = f"{output_prefix}.snp.subset.vcf.gz"
    bcftool_extract_snp(vcf_file, extract_file,strains)

    # Extract phenotypic data
    extract_phenotypic_data(phenotype_file, strains)
    print("Summary statistics before filtering:")
    report_snp_data_statistics(extract_file)

    # Filter snp data
    filtered_out = f"{output_prefix}.snp.filtered.vcf"
    filter_snp_data(extract_file, filtered_out, missing_threshold=0.95, maf_threshold=0.18)
    
    # Report snp data statistics
    print("Summary statistics after filtering:")
    report_snp_data_statistics(filtered_out)

    print("")
    print("Data extraction completed.")

if __name__ == "__main__":
    main()