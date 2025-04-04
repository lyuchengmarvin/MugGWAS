# This script annotates variants with annovar
# Time: 2025-02-12
# Author: Yu-Cheng Lin

## This script run annovar externally
import os

## First function is to convert the vcf file to annovar input format
def convert_vcf_to_annovar(annovar_dir, input_dir, vcf_prefix):
    """
    Converts a VCF file to annovar input format.
    Args:
        annovar_dir (str): Path to the annovar directory.
        input_dir (str): Path to the input VCF file.
        vcf_prefix (str): Output prefix for the converted annovar input file.
    """
    # Check if the annovar directory exists
    if not os.path.exists(annovar_dir):
        raise FileNotFoundError(f"Annovar directory {annovar_dir} does not exist.")
    # Check if the input VCF file exists
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input VCF file {input_dir} does not exist.")
    # Check if the output directory exists, if not create it
    data_dir = os.path.dirname(input_dir)
    output_dir = os.path.join(data_dir, 'annovar_files/')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Convert the VCF file to annovar input format
    convert_cmd = f"perl {annovar_dir}convert2annovar.pl -format vcf4 {input_dir} -allsample -outfile {output_dir}{vcf_prefix}"
    os.system(convert_cmd)


## The second function is to build the annovar database
def build_annovar_db(annovar_dir, db_dir, ref_prefix):
    """
    Builds the annovar database.
    Args:
        annovar_dir (str): Path to the annovar directory.
        db_dir (str): Path to the annovar database directory.
        ref_prefix (str): Output prefix for the annovar database.
    """
    # Check if the annovar directory exists
    if not os.path.exists(annovar_dir):
        raise FileNotFoundError(f"Annovar directory {annovar_dir} does not exist.")
    # Check if the database directory exists
    if not os.path.exists(db_dir):
        raise FileNotFoundError(f"Database directory {db_dir} does not exist.")
    # Check if the reference fasta file exists
    ref_fasta = os.path.join(db_dir, f"{ref_prefix}.fna")
    if not os.path.exists(ref_fasta):
        raise FileNotFoundError(f"Reference fasta file {ref_fasta} does not exist.")
    # Check if the reference gff file exists
    ref_gff = os.path.join(db_dir, f"{ref_prefix}.gff3")
    if not os.path.exists(ref_gff):
        raise FileNotFoundError(f"Reference gff file {ref_gff} does not exist.")
    
    # Build annovar database
    # Use `gff3ToGenePred` to convert gff3 to genePred format
    gff3ToGenePred_cmd = f"gff3ToGenePred {ref_gff} {db_dir}{ref_prefix}.refGene0.txt && nl {db_dir}{ref_prefix}.refGene0.txt > {db_dir}{ref_prefix}_refGene.txt && rm {db_dir}{ref_prefix}.refGene0.txt"
    os.system(gff3ToGenePred_cmd)
    # Extract mRNA sequences from the reference fasta file
    retrievemrna_cmd = f"perl {annovar_dir}retrieve_seq_from_fasta.pl {db_dir}{ref_prefix}_refGene.txt -format ensGene -seqfile {ref_fasta} -outfile {db_dir}{ref_prefix}_refGeneMrna.fa"
    os.system(retrievemrna_cmd)

## The third function is to annotate the avinput files
def annotate_avinput(annovar_dir, avinput_dir, ref_prefix, db_dir):
    """
    Annotates avinput files with annovar.
    Args:
        annovar_dir (str): Path to the annovar directory.
        avinput_dir (str): Path to the avinput directory.
        db_dir (str): Path to the annovar database directory.
    """
    # Check if the avinput directory exists
    if not os.path.exists(avinput_dir):
        raise FileNotFoundError(f"Annovar input file directory {avinput_dir} does not exist.")
    # Check if the database directory exists
    if not os.path.exists(db_dir):
        raise FileNotFoundError(f"Database directory {db_dir} does not exist.")
    # Check if the database files exist
    db_files = [ref_prefix+'_refGeneMrna.fa', ref_prefix+'_refGene.txt']
    # Check if the database files exist
    for db_file in db_files:
        if not os.path.exists(os.path.join(db_dir, db_file)):
            raise FileNotFoundError(f"Database file {db_file} does not exist in {db_dir}.")
    
    # Annotate avinput files
    avinput_files = [f for f in os.listdir(avinput_dir) if f.endswith('.avinput')]
    # annotate each avinput file
    for avinput_file in avinput_files:
        annovar_cmd = f"perl {annovar_dir}annotate_variation.pl -geneanno -buildver {ref_prefix} {avinput_dir}{avinput_file} {db_dir}"
        os.system(annovar_cmd)

## Main function
## User inputs
# path to the annovar directory
# annovar_dir = '/Users/linyusheng/MugGWAS/scripts/annovar/'
# the directory where the reference files are located
# db_dir = '/Users/linyusheng/MugGWAS/data/LE18_22/'
# path to the vcf file
# input_dir = '/Users/linyusheng/MugGWAS/data/graz_LE.snp.vcf'
# output prefix or the converted annovar input file
# vcf_prefix = 'graz_LE'
# output prefix for the annovar database
# ref_prefix = 'LE18_22'

def run_annovar(annovar_dir, input_dir, db_dir, vcf_prefix, ref_prefix):
    # the directory where the avinput files are located
    avinput_dir = os.path.join(os.path.dirname(input_dir), 'annovar_files/')

    # Convert the VCF file to annovar input format
    print("Converting VCF file to annovar input format...")
    print("")
    convert_vcf_to_annovar(annovar_dir, input_dir, vcf_prefix)
    print("")
    print(f"The VCF file has been converted and saved to {avinput_dir}.")
    print("")
    # Build the annovar database
    build_annovar_db(annovar_dir, db_dir, ref_prefix)
    print(f"Database has been built and saved to {db_dir}.")
    print("")
    # Annotate the avinput files
    print("Annotating avinput files...")
    print("")
    annotate_avinput(annovar_dir, avinput_dir, ref_prefix, db_dir)
    num_avinput_files = len([f for f in os.listdir(avinput_dir) if f.endswith('.avinput')])
    print(f"{num_avinput_files} samples have been annotated and saved to {avinput_dir}.")
