# This script takes the output of MugGWAS and runs pyseer on it.
# Author: Yucheng Marvin Lin
# Time: 2025-04-14
# Arguments:
# --phenotypes: The path to the phenotype file.
# --similarity: The path to the similarity matrix built from phylogeny.
# --mutation: The path to the gene mutation summary table.
# --output: The path to the output directory.


## This script will run pyseer externally in the terminal
import subprocess
import logging
import time
from pathlib import Path
import shlex  # Add this import for shlex.join

## Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## Function to parse mutation summary table
def parse_mutation_summary(mutation_summary_file):
    """
    Convert values to numeric format in the mutation summary table.
    This function reads a mutation summary file and converts the values to numeric format.
    The input file should be a tab-delimited file with the first column as the gene name and the rest as the mutation values, including wildtype, mutation, missense, nonsense, nonstop, or silent.
    The output file will convert the values to numeric format, where 0 represents wildtype and 1 represents mutation, and stored in the same directory as the input file.
    The output file will be named as <input_file_name>_numeric.txt.
    The function will also log the conversion process and the number of mutations found in the file.

    Args:
        mutation_summary_file (str): Path to the mutation summary file.
    """

    # Convert mutation_summary_file to a Path object
    mutation_summary_path = Path(mutation_summary_file)

    # Check if the input file exists
    if not mutation_summary_path.exists():
        raise FileNotFoundError(f"Input mutation summary file {mutation_summary_file} does not exist.")
    
    # Read the mutation summary file
    with mutation_summary_path.open('r') as f:
        lines = f.readlines()
    
    # Skip the header
    header = lines[0]
    data_lines = lines[1:]
    
    # Convert the values to numeric format
    numeric_lines = [header.strip()]  # Keep the header as is
    skipped_genes = 0
    for line in data_lines:
        values = line.strip().split('\t')
        gene_name = values[0]
        mutation_values = [0 if value == 'wildtype' else 1 for value in values[1:]]
        # Count the number of mutations
        mutation_count = sum(mutation_values)
        if mutation_count > 0:
            numeric_line = [gene_name] + mutation_values
            numeric_lines.append('\t'.join(map(str, numeric_line)))
            logging.info(f"Gene {gene_name} has a mutation rate of {mutation_count/len(mutation_values)}.")
        else:
            skipped_genes += 1
            logging.info(f"Gene {gene_name} has no mutations in the population. Skipping this gene.")
    
    logging.info(f"Integrating {len(numeric_lines)-1} genes to run GWAS on pyseer.")

    # Write the numeric values to a new file
    output_file = mutation_summary_path.with_name(mutation_summary_path.stem + '_filtered_numeric.txt')
    with output_file.open('w') as f:
        f.write('\n'.join(numeric_lines))
    
    logging.info(f"Skipped {skipped_genes} genes with no mutations.")
    logging.info(f"Converted mutation summary file {mutation_summary_file} to numeric format and saved as {output_file}.")

## Main function to run pyseer
def run_pyseer(phenotype_file, similarity_file, mutation_summary_file, output_dir):
    """
    Run pyseer on the provided phenotype file, similarity matrix, and mutation summary file.
    The function will create an output directory if it does not exist and run pyseer with the specified parameters.
    
    Args:
        phenotype_file (str): Path to the phenotype file.
        similarity_file (str): Path to the similarity matrix file.
        mutation_summary_file (str): Path to the mutation summary file.
        output_dir (str): Path to the output directory.
    """
    # Start time
    start_time = time.time()
    logging.info(f"Start running GWAS with pyseer")
    
    # Convert input paths to Path objects
    phenotype_path = Path(phenotype_file)
    similarity_path = Path(similarity_file)
    mutation_summary_path = Path(mutation_summary_file)
    output_dir_path = Path(output_dir)

    # Check if the input files exist
    if not phenotype_path.exists():
        raise FileNotFoundError(f"Input phenotype file {phenotype_file} does not exist.")
    if not similarity_path.exists():
        raise FileNotFoundError(f"Input similarity matrix file {similarity_file} does not exist.")
    if not mutation_summary_path.exists():
        raise FileNotFoundError(f"Input mutation summary file {mutation_summary_file} does not exist.")
    
    # Create the output directory if it does not exist
    output_dir_path.mkdir(parents=True, exist_ok=True)
    output_file = output_dir_path / 'pyseer_results.txt'
    
    # Convert mutation summary table to numeric format
    parse_mutation_summary(mutation_summary_file)
    
    # Get the numeric mutation summary file path
    numeric_mutation_summary_file = mutation_summary_path.with_name(mutation_summary_path.stem + '_filtered_numeric.txt')
    
    # Run pyseer command
    pyseer_command = [
        "pyseer",
        "--lmm",
        "--phenotypes", str(phenotype_path),
        "--similarity", str(similarity_path),
        "--pres", str(numeric_mutation_summary_file)
    ]
    pyseer_command_str = shlex.join(pyseer_command) + f" > {output_file}"
    
    logging.info(f"Running pyseer with command: {pyseer_command_str}")
    
    # Run the command in a subprocess
    try:
        subprocess.run(pyseer_command_str, shell=True, check=True)
        logging.info("Pyseer run completed successfully.")
        logging.info(f"GWAS results are saved in {output_dir_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Pyseer run failed with error: {e}")
    
    # End logging
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    logging.info(f"Script completed in {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
    logging.info("Finished running pyseer.")
    logging.info("GWAS analysis completed.")



