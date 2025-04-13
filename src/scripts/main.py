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
    from muggwas.
from annotate_variants import run_annovar
from compile_variants_by_gene import compile_gene_mutations, write_gene_mutation_summary
from estimate_pop_structure import phylogeny2distmatrix

