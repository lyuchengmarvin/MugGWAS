# This is a script that compiles the variants by gene from the variant files
# Author: Yu-Cheng Lin
# Time: 2025-02-12

import gffutils
import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time


class GeneVariantAnalyzer:
    def __init__(self, gff_file):
        """
        Initialize the GeneVariantAnalyzer with a GFF3 file.

        Args:
            gff_file (str): Path to the GFF3 file.
        """
        self.gff_file = gff_file
        self.gene_annotations = self.extract_gene_annotations()

    def extract_gene_annotations(self):
        """
        Extracts the gene ID and annotations from a GFF3 file.

        Returns:
            dict: A dictionary where keys are gene IDs and values are dictionaries with the gene annotation and an empty tuple for storing mutations.
        """
        try:
            db = gffutils.create_db(self.gff_file, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
        except Exception as e:
            raise ValueError(f"Failed to create database from GFF3 file: {e}")

        try:
            if not any(feature.featuretype in ['CDS', 'gene'] for feature in db.all_features()):
                raise ValueError("No CDS or gene features found in the GFF3 file.")
        except Exception as e:
            raise ValueError(f"Error while checking features in GFF3 file: {e}")

        gene_annotations = {}
        for gene in db.features_of_type(['CDS', 'gene']):
            gene_id = gene.id
            annotation = gene.attributes.get('Name', [''])[0]
            if gene_id not in gene_annotations:
                gene_annotations[gene_id] = {'annotation': annotation, 'mutations': ()}
            else:
                if gene_annotations[gene_id]['annotation'] != annotation:
                    print(f"Warning: Gene ID {gene_id} has multiple annotations. Keeping the first one.")
        return gene_annotations

    def extract_gene_mutations(self, annovar_file):
        """
        Extracts gene mutations from an ANNOVAR output file and updates the gene annotations.

        Args:
            annovar_file (str): Path to the ANNOVAR output file.

        Returns:
            dict: Updated gene annotations with mutations added.
        """
        with open(annovar_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                fields = line.strip().split('\t')
                gene_id = fields[2].split(':')[0]
                if gene_id not in self.gene_annotations:
                    continue
                mutation_info = fields[1]
                current_mutations = self.gene_annotations[gene_id]['mutations']
                self.gene_annotations[gene_id]['mutations'] = current_mutations + (mutation_info,)
        return self.gene_annotations

    def determine_mutation_type(self, gene_mutations, model='multiple'):
        """
        Determines the mutation type based on the mutation information.

        Args:
            gene_mutations (tuple): A tuple containing mutation information.
            model (str): To return binary or multiple mutation types. Default is 'multiple'.

        Returns:
            str: The mutation type.
        """
        if model == 'binary':
            if any(mut in gene_mutations for mut in ['stopgain', 'stoploss', 'nonsynonymous SNV']):
                return 'mutated'
            else:
                return 'wildtype'
        elif model == 'multiple':
            if 'stopgain' in gene_mutations:
                return 'nonsense'
            elif 'stoploss' in gene_mutations:
                return 'nonstop'
            elif 'nonsynonymous SNV' in gene_mutations:
                return 'missense'
            elif 'synonymous SNV' in gene_mutations:
                return 'silent'
            else:
                return 'wildtype'

    def create_gene_mutation_dict(self, gene_annotations, model='multiple'):
        """
        Creates a dictionary with gene names as keys and mutation types as values.

        Args:
            gene_annotations (dict): A dictionary where keys are gene IDs and values are dictionaries with annotations and mutations.
            model (str): To return binary or multiple mutation types. Default is 'multiple'.

        Returns:
            dict: A dictionary where keys are gene names and values are mutation types.
        """
        gene_mutation_dict = {}
        for gene_id, info in gene_annotations.items():
            mutations = info['mutations']
            mutation_type = self.determine_mutation_type(mutations, model)
            gene_mutation_dict[gene_id] = mutation_type
        
        return gene_mutation_dict



## Main functions
# User inputs
# # Directory containing the ANNOVAR output files
# annovar_output_dir = '/Users/linyusheng/MugGWAS/data/annovar_files'
# # Read gff3 to build gene maps
# gff_file = '/Users/linyusheng/MugGWAS/data/LE18_22/LE18_22.gff3'
# # Write the mutation types to a tab delimited file
# output_file = '/Users/linyusheng/MugGWAS/data/gene_mutation_summary.txt'


def process_sample(sample, annovar_output_dir, gff_file, model):
    """
    A function for parallel computing.
    Processes a single sample to extract gene mutations and determine mutation types.

    Args:
        sample (str): The sample file name.
        annovar_output_dir (str): Directory containing the ANNOVAR output files.
        gff_file (str): Path to the GFF3 file.
        model (str): To return binary or multiple mutation types.

    Returns:
        tuple: A tuple containing the sample name and its gene mutation dictionary.
    """
    sample_name = sample.split('.')[1]  # Extract sample name from the file name
    sample_path = os.path.join(annovar_output_dir, sample)
    
    # Initialize a gene map with the GFF3 file
    analyzer = GeneVariantAnalyzer(gff_file)

    # Extract gene mutations for the sample
    gene_anno_mut = analyzer.extract_gene_mutations(sample_path)
    
    # Determine the mutation types for the sample
    return sample_name, analyzer.create_gene_mutation_dict(gene_anno_mut, model)

def compile_gene_mutations(annovar_output_dir, gff_file, model='multiple'):
    """
    Compiles the gene mutations from ANNOVAR output files in parallel.

    Args:
        annovar_output_dir (str): Directory containing the ANNOVAR output files.
        gff_file (str): Path to the GFF3 file.
        model (str): To return binary or multiple mutation types. Default is 'multiple'.

    Returns:
        sample_mut_dict (dict): A dictionary where keys are sample names and values are dictionaries with gene mutation types.
    """
    # Start timing
    start_time = time.time()  

    # Get the list of ANNOVAR output files
    sample_list = [f for f in os.listdir(annovar_output_dir) if f.endswith('exonic_variant_function')]

    # Use ProcessPoolExecutor for parallel processing
    sample_mut_dict = {}
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        results = executor.map(process_sample, sample_list, [annovar_output_dir]*len(sample_list), [gff_file]*len(sample_list), [model]*len(sample_list))
        for sample_name, gene_mut_dict in results:
            sample_mut_dict[sample_name] = gene_mut_dict
    
    end_time = time.time()  # End timing
    print(f"Time elapsed for compiling gene mutations: {end_time - start_time:.2f} seconds")
    print(f"Total number of samples processed: {len(sample_mut_dict)}")

    return sample_mut_dict

def write_gene_mutation_summary(sample_mut_dict, output_file):
    """
    Writes the gene mutation summary to a tab delimited file.

    Args:
        sample_mut_dict (dict): A dictionary where keys are sample names and values are dictionaries with gene mutation types.
        output_file (str): Path to the output file where the mutation types for each sample across all genes will be saved.
    Returns:
        An output file with the rows as gene names and columns as sample names, with the mutation types for each sample across all genes.
    """
    # Create a dictionary to store the mutation types for each gene across all samples
    gene_mutation_types = {}
    
    # Iterate over each sample and extract mutation types
    for sample_name, gene_mutations in sample_mut_dict.items():
        for gene, mutation_type in gene_mutations.items():
            if gene not in gene_mutation_types:
                gene_mutation_types[gene] = {}
            if sample_name not in gene_mutation_types[gene]:
                gene_mutation_types[gene][sample_name] = mutation_type
            else:
                # If the sample already exists, combine the mutation types
                raise ValueError(f"Sample {sample_name} already exists for gene {gene}. Please check the data.")
    
    # Write the mutation types to a tab delimited file
    with open(output_file, 'w') as f:
        # Write header
        sample_names = list(sample_mut_dict.keys())
        f.write("Gene\t"+'\t'.join(sample_names)+'\n')
        
        # Write mutation types for each sample across all genes
        for gene, sample_mutation in gene_mutation_types.items():
            # Create a row for the gene
            row = [gene]
            # Add mutation types for each sample
            for sample_name in sample_names:
                row.append(sample_mutation[sample_name])
            # Write the row to the file
            f.write('\t'.join(row) + '\n')
    print(f"Gene mutation summary has been written to {output_file}.")
    print("")