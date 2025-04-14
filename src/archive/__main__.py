#!/usr/bin/env python3
"""
MugGWAS: A pipeline for GWAS analysis using pylogeny and gene mutations from non-model organisms.

The script implements the full MugGWAS pipeline for annotating variants, 
compiling gene mutations, and estimating population structure to perform GWAS analysis.
"""

import os
import sys
import argparse
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("muggwas.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Try to import the necessary modules, with error messages if missing:
try:
    import pandas as pd
    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor
    import gffutils
    import dendropy
except ImportError as e:
    logging.error(f"Required module not found: {e}")
    logging.error("Please install the required modules: pandas, multiprocessing, gffutils, dendropy.")
    sys.exit(1)

# Import MugGWAS modules
try:
    from src.scripts.annotate_variants import run_annovar
    from src.scripts.compile_variants_by_gene import compile_gene_mutations, write_gene_mutation_summary
    from src.scripts.estimate_pop_structure import phylogeny2distmatrix
except ImportError as e:
    logging.error(f"Error importing MugGWAS modules: {e}")
    logging.error("Please ensure that the MugGWAS package is correctly installed.")
    sys.exit(1)

# Command line arguments
def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="MugGWAS: A pipeline for GWAS analysis using pylogeny and gene mutations from non-model organisms.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Input options
    input_group = parser.add_argument_group("Input Options")
    input_group.add_argument('--vcf', required=True, help="Path to the input VCF file.")
    input_group.add_argument('--db_dir', required=True, help="Path to the directory containing the reference files.")
    input_group.add_argument('--gff_file', required=True, help="Path to the GFF3 file.")
    input_group.add_argument('--phylogeny', required=True, help="Path to the phylogenetic tree file.")

    # mode options
    mode_group = parser.add_argument_group("Mode Options")
    mode_group.add_argument('--mode', choices=['binary', 'multiple'], default='binary', help="Output mode for gene mutation categories.")

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument('--vcf_prefix', required=True, help="Output prefix for the converted annovar input file.")
    output_group.add_argument('--ref_prefix', required=True, help="Output prefix for the annovar database.")
    output_group.add_argument('--out_gene_table', required=True, help="Path to the output file for gene mutation summary.")
    output_group.add_argument('--out_dist_matrix', required=True, help="Path to the output file for distance matrix.")

    # Logging options
    logging_group = parser.add_argument_group("Logging Options")
    logging_group.add_argument('--log', default='muggwas.log', help="Path to the log file.")

# Main function
def main():
    """
    Main entrypoint for the MugGWAS pipeline.
    """
    start_time = time.time()
    logging.info("Starting MugGWAS pipeline...")
    logging.info("Current working directory: %s", os.getcwd())
    logging.info("Python version: %s", sys.version)
    logging.infor(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    # Parse command line arguments
    parser = parse_arguments()
    args = parser.parse_args()

    # Start the pipeline
    ## Run ANNOVAR
    #run_annovar(input_dir, db_dir, vcf_prefix, ref_prefix)
    logging.info("Running ANNOVAR...")
    run_annovar(args.vcf, args.db_dir, args.vcf_prefix, args.ref_prefix)
    logging.info("ANNOVAR completed successfully.")
    ## Compile gene mutations
    logging.info("Compiling gene mutations...")
    gene_mutation_summary = compile_gene_mutations(args.gff_file, annovar_output_dir, args.mode)
    logging.info("Gene mutations compiled successfully.")
    ## Write gene mutation summary
    logging.info("Writing gene mutation summary...")
    write_gene_mutation_summary(gene_mutation_summary, args.out_gene_table)
    logging.info(f"Gene mutation summary written successfully.")
    ## Estimate population structure
    logging.info("Estimating population structure...")
    phylogeny2distmatrix(args.phylogeny, args.out_dist_matrix)
    logging.info("Population structure estimation completed successfully.")

    # End the pipeline
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    logging.info("MugGWAS pipeline completed successfully.")
    logging.info("Total elapsed time: %d hours, %d minutes, %d seconds", int(hours), int(minutes), int(seconds))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

