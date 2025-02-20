# This is a script that compiles the variants by gene from the variant files
# Author: Yu-Cheng Lin
# Time: 2025-02-12

import gffutils
import pysam

# Read function that reads gff3 file for the reference genome
def extract_gene_positions(gff_file):
    """
    Extracts the contig, start, and end positions of all genes from a GFF3 file.

    Args:
        gff_file (str): Path to the GFF3 file. The file must contain contig names, coding gene features (CDS), gene IDs, start, and end positions.

    Returns:
        dict: A dictionary where keys are gene IDs and values are dictionaries with contig names as keys and tuples of (start, end) positions as values.
    """
    # Create a database from the GFF3 file
    db = gffutils.create_db(gff_file, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
    
    gene_positions = {}
    
    # Check if 'CDS' or 'gene' is in the features of the GFF file
    if not any(feature.featuretype in ['CDS', 'gene'] for feature in db.all_features()):
        raise ValueError("no CDS or gene in gff file")
    
    # Iterate over all genes in the database
    for gene in db.features_of_type(['CDS', 'gene']):
        gene_id = gene.id
        contig = gene.seqid
        start = gene.start
        end = gene.end
        if gene_id not in gene_positions:
            gene_positions[gene_id] = {}
        gene_positions[gene_id][contig] = (start, end)
    
    return gene_positions


# Read function that parse the vcf file
def parse_vcf(vcf_file):
    """
    Parses a VCF file and creates a dictionary with keys as sites and values as dictionaries containing alleles for each sample.

    Args:
        vcf_file (str): Path to the VCF file (can also handle a .gz file).

    Returns:
        dict: A dictionary where keys are tuples of (chromosome, position) and values are dictionaries with sample names as keys and alleles as values. Allele (0,0) is homozygous reference, (0,1) is heterozygous, and (1,1) is also homozygous alternative.
    """
    vcf = pysam.VariantFile(vcf_file)
    site_dict = {}

    for record in vcf:
        # Create a snp id that concatenate chromosome, position, ref and alt alleles.
        site = str(record.chrom)+":"+str(record.pos)+":"+str(record.ref)+":"+str(record.alts[0])
        # Initalize the site in the dictionary
        site_dict[site] = {}
        # Iterate over all samples in the VCF file and add the alleles to the dictionary
        for sample in record.samples:
            alleles = record.samples[sample]['GT']
            site_dict[site][sample] = alleles

    return site_dict
