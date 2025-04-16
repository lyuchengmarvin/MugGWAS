#!/usr/bin/env python3

# This script changes the chromosome name of the vcf file to a user-specified one.
# It is intended to be used with the muggwas pipeline.
# The script takes the following arguments:
# -i: input vcf file
# -o: output vcf file
# -c: chromosome name to change to
# -h: help message

import argparse
import os
import sys
import re
import logging
import gzip

def parse_args():
    parser = argparse.ArgumentParser(description="Change chromosome name in VCF file.")
    parser.add_argument("-i", "--input", required=True, help="Input VCF file")
    parser.add_argument("-o", "--output", required=True, help="Output VCF file")
    parser.add_argument("-c", "--chromosome", required=True, type=str, help="Chromosome name to change to")
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("change_vcf_chrm.log")
        ]
    )
    return logging.getLogger(__name__)

def open_file(file_path, mode):
    """
    Open a file, supporting both plain text and gzip-compressed files.

    Args:
        file_path (str): Path to the file.
        mode (str): Mode to open the file ('r' for reading, 'w' for writing).

    Returns:
        file object: Opened file object.
    """
    if file_path.endswith(".gz"):
        return gzip.open(file_path, mode + "t")  # Add 't' for text mode
    return open(file_path, mode)

def change_chromosome_name(input_file, output_file, new_chromosome):
    """
    Change the chromosome name in the VCF file.

    Args:
        input_file (str): Path to the input VCF file.
        output_file (str): Path to the output VCF file.
        new_chromosome (str): New chromosome name.
    """
    with open_file(input_file, "r") as infile, open_file(output_file, "w") as outfile:
        for line in infile:
            if line.startswith("##contig=<ID="):
                # Modify the contig header line
                line = re.sub(r"##contig=<ID=[^,]+", f"##contig=<ID={new_chromosome}", line)
            elif not line.startswith("#"):
                # Change the chromosome name in the data lines
                parts = line.split("\t")
                parts[0] = new_chromosome
                line = "\t".join(parts)
            outfile.write(line)

def main():
    args = parse_args()
    logger = setup_logging()

    # Check if input file exists
    if not os.path.isfile(args.input):
        logger.error(f"Input file {args.input} does not exist.")
        sys.exit(1)

    # Change chromosome name
    change_chromosome_name(args.input, args.output, args.chromosome)
    logger.info(f"Chromosome name changed to {args.chromosome} in {args.output}")
    # Check if output file was created
    if os.path.isfile(args.output):
        logger.info(f"Output file {args.output} created successfully.")
    else:
        logger.error(f"Failed to create output file {args.output}.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# This script is part of the muggwas pipeline.
