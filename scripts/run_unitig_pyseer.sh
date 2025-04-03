#!/bin/bash
#SBATCH --job-name=pyseer_unitig
#SBATCH --mail-user=lyucheng@umich.edu
#SBATCH --mail-type=BEGIN,FAIL,END
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=180G
#SBATCH --time=01-12:00:00
#SBATCH --account=vdenef0
#SBATCH --partition=standard
#SBATCH --export=ALL
#SBATCH --error=error-%x-%j.log
#SBATCH --output=%x-%j.log

## Define directories
pheno_dir='/nfs/turbo/lsa-vdeneflab/vdenef-turbo/lyucheng/gene_trait_linkage'
output_dir='/home/lyucheng/varcall_LE/pyseer/unitig'
list_file='file_list.txt'
# List SNPs.txt files in the input directory
#ls "$pheno_dir"/phenotypes/*.txt > "$list_file"

# Read the list of files and run the command iteratively in a for loop
while IFS= read -r file_path; do
    file_name=$(basename "$file_path" .txt) 
    input_file_path="$pheno_dir/phenotypes/$file_name.txt"
    output_file_path="$output_dir/$file_name.unitig.txt"
    unitig_pattern_path="$output_dir/$file_name.unitig_pattern.txt"
    
    # construct the command string
    command="pyseer --lmm --phenotypes \"$input_file_path\" \
    --kmers unitig/LE.unitigs.pyseer.txt.gz \
    --similarity phylogeny_distances.tsv \
    --output-patterns \"$kmer_pattern_path\" \
    --covariates LE_covariates.txt \
    --cpu 8 > \"$output_file_path\""

    # executes the command string
    eval $command

    # Check command success and print messages
    if [ $? -eq 0 ]; then
        echo "Successfully processed $file_name"
    else
        echo "Error processing $file_name"
    fi
done < "$list_file"
