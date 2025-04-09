# **Mutated-gene Genome-Wide Association Study (MugGWAS)**

MugGWAS identifies potential causal mutations for phenotypic change through testing associations between mutated genes and phenotypic values. Please refer to these files for the implementation of the tool.

**Tutorial file:**
- directory: `tutorial/tutorial.ipynb`
- This is a tutorial file that implements the tool based on tutorial data.

**Tutorial data:**
- directory: `data/`
- Reference files: `data/LE18_22/` 
  - `LE18_22.fna`: The genome sequence for the reference assembly
  - `LE18_22.gff3`: The gene annotation for the reference assembly
  - `LE18_22_refGene.txt`: One of the database files for ANNOVAR.
  - `LE18_22_refGeneMrna.fa`: One of the database files for ANNOVAR.
- Variant file: `data/graz_LE.snp.vcf`
  - The VCF file resulted from a variant calling pipeline for the samples of interest. It contains variant information for multiple samples.
- ANNOVAR annotation outputs: `data/annovar_files/'
  - `<sample_id>.avinput`: The variant input files for ANNOVAR, converted from the vcf file. There is one output per sample.
  - `<sample_id>.avinput.variant_function`: ANNOVAR output, returning the position of a mutation on a gene.
  - `<sample_id>.avinput.exonic_variant_function`: ANNOVAR output, returning mutation effects on translation, namely synonymous, nonsynonymous, stop codon gain, or stop codon loss.
- MugGWAS output: `data/gene_mutation_summary.txt`
  - This table is the output of module 1 for MugGWAS. This documents the mutation types for each gene across all samples. This will be used for GWAS in module 2.
