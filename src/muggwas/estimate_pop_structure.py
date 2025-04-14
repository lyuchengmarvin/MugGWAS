# This is a script that estimates the population structure from phylogeny or kinship
# Author: Yucheng Marvin Lin
# Time: 2025-04-03

## This script run pyseer externally
import os
import dendropy
import pandas as pd

## User input:
# phylogeny_dir = "path_to/phylogeny_file.nwk"
# output_dir = "path_to/output_directory/phylogeny_distances.tsv"

## Phylogeny-based method: Extract distance matrix from a phylogeny
def phylogeny2distmatrix(phylogeny_dir, output_dir):
    """
    Extract a distance matrix from a phylogeny. Since MugGWAS will implement the FaST-LMM model in pyseer, the similarities based on the shared branch length between each pair's MRCA and the root will be calculated.
    Args:
        phylogeny_dir (str): Path to the phylogeny file.
        output_dir (str): Path to the output directory.
    """
    # Check if the phylogeny file exists
    if not os.path.exists(phylogeny_dir):
        raise FileNotFoundError(f"Phylogeny file {phylogeny_dir} does not exist.")
    
    # Load the phylogeny
    tree = dendropy.Tree.get(path=phylogeny_dir, schema="newick", preserve_underscores=True)
    
    dist_matrix = {}

    # Extract distance matrix
    pdm = tree.phylogenetic_distance_matrix()

    for idx1, taxon1 in enumerate(tree.taxon_namespace):
        dist_matrix[taxon1.label] = {}
        for taxon2 in tree.taxon_namespace:
            if taxon2.label not in dist_matrix[taxon1.label].keys():
                mrca = pdm.mrca(taxon1, taxon2)
                dist_matrix[taxon1.label][taxon2.label] = mrca.distance_from_root()

    # Convert to DataFrame, reindex, and save to tsv
    dist_df = pd.DataFrame(dist_matrix)
    dist_df = dist_df.reindex(dist_df.columns)
    dist_df.to_csv(output_dir, sep="\t", index=True)


## User input:
# core_gene_snp_dir = "path_to/core_gene_snp.vf.gz"
# output_dir = "path_to/output_directory/"

## Kinship-based method: Calculate kinship matrix from the presence and absence of SNPs