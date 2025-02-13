# This is a script that compiles the variants by gene from the variant files
# Author: Yu-Cheng Lin
# Time: 2025-02-12

import os
from Bio import SeqIO
import pysam

# Read function that reads gff3 file for the reference genome
def read_gff3(gff3_file):
    gene_dict = {}
    with open(gff3_file, 'r') as gff3:
        for line in gff3:
            if not line.startswith('#'):
                line = line.strip().split('\t')
                if line[2] == 'gene':
                    gene_id = line[8].split(';')[0].split('=')[1]
                    gene_dict[gene_id] = {'start': int(line[3]), 'end': int(line[4])}
    return gene_dict

# Read function that reads the vcf
def read_vcf(vcf_file, gene_dict):
    variant_dict = {}
    for gene in gene_dict:
        variant_dict[gene] = {}
    vcf = pysam.VariantFile(vcf_file)
    for record in vcf:
        for gene in gene_dict:
            if gene_dict[gene]['start'] <= record.pos <= gene_dict[gene]['end']:
                for alt in record.alts:
                    variant_dict[gene][alt] = variant_dict[gene].get(alt, 0) + 1
    return variant_dict
