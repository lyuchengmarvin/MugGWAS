# This is a script that compiles the variants by gene from the variant files
# Author: Yu-Cheng Lin
# Time: 2025-02-12

import os
from Bio import SeqIO

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

# Read function that reads the vcf and compile the variants by gene
def read_vcf(vcf_file, gene_dict):
    gene_variants = {}
    with open(vcf_file, 'r') as vcf:
        for line in vcf:
            if not line.startswith('#'):
                line = line.strip().split('\t')
                gene_id = line[0]
                pos = int(line[1])
                ref = line[3]
                alt = line[4]
                if gene_id in gene_dict:
                    if gene_id not in gene_variants:
                        gene_variants[gene_id] = []
                    gene_variants[gene_id].append({'pos': pos, 'ref': ref, 'alt': alt})
    return gene_variants
    
