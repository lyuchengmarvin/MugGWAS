This is the documentation on the functionality of this package and the prerequisite for the usage.

## Motivation

Understanding the genetic basis of a trait is central to many biological research that help gain mechanismtic insight into complex biological phenomena. For instance, the discovery of genetic loci that contribute to antibiotic resistance could better our knowledge for how important pathogens evolve to escape medicinal application. 

Most association tools classify raw genetic variants (like single nucleotide polymorphisms or structural variants) into reference or alternative genotypes, then perform statistical tests to infer associations between particular variants and phenotypes. However, genome-wide analyses typically require large sample sizes for statistical power—a major challenge for organisms that are difficult to culture or traits that are challenging to measure. Alternative approaches test associations between phenotypes and gene presence/absence, but these methods don't capture finer details like important mutations that potentially disrupt gene function.

Mutated-gene Genome-Wide Association Study (MugGWAS) addresses these limitations by offering a non-model-organism-friendly pipeline to infer gene-trait associations. By annotating disruptive mutation types (nonsense, missense, stopgain, or nonstop), MugGWAS identifies putative gene dysfunctions associated with phenotypic changes. This approach conserves statistical power by avoiding tests on variants that either (1) don't affect function at the gene level or (2) result in disruption of the same gene, allowing users to identify putative gene mutations driving phenotypic changes without the large statistical power required for per-nucleotide genome-wide tests.

## Functionality

**Annotate the variants:**
- Module: annotate_variation
- External tool: ANNOVAR, users need to [download](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) this themselves.
- Functionality: Annotate the variants for each sample to infer their mutation types on a gene. Compile these mutations gene by gene.

**Build gene mutation table:**
- Module: compile_variants_by_gene
- Functionality: 
  1. Determine the mutation types for each gene across all samples. Users can specify if they want to output 'binary genotypes', i.e. mutated or wildtype, or 'multiple genotypes', i.e. nonsense, nonstop, missense, silent, or wildtype. MugGWAS now uses a binary classification (mutant or wildtype) for GWAS.
  2. Output a gene annotation table for the users' reference.

**Estimate the population structure effect:**
- Module: estimate_pop_structure
- Functionality: Infer population structure based on phylogenetic distances. Since MugGWAS will use a linear mixed model, the distance will be estimated from the shared branch length between the MRCA and the root.

**Run GWAS with pyseer:**
- Module: run_pyseer_COG
- Functionality: Run mixed effect model from `pyseer` to infer gene-trait association.


## Description of the Data Structure

**Tutorial file:**

- directory: `tutorial/tutorial.ipynb`
- This is a tutorial for the full implementation of the MugGWAS pipeline.

**Tutorial data:**

- directory: `data/pyseer_dataset/`
- Reference files: `data/ref_prefix/` 
  - `ref_prefix.fna`: The genome sequence for the reference assembly.
  - `ref_prefix.gff3`: The gene annotation for the reference assembly.
  - `ref_prefix_refGene.txt`: One of the database files for ANNOVAR (produced by the annotate_variants module in MugGWAS).
  - `ref_prefix_refGeneMrna.fa`: One of the database files for ANNOVAR (produced by the annotate_variants module in MugGWAS).
- Variant file:
  - `vcf_prefix.filtered.vcf.gz`: The VCF file resulted from a variant calling tool such as GATK HaplotypeCaller or FreeBayes containing variant information for multiple samples. This data has been filtered accroding to the threshold of 5% missing value and 1% minor allele frequency.
- ANNOVAR annotation outputs: 
  - These are produced by the annotate_variants module in MugGWAS.
  - `<sample_id>.avinput`: The variant input files for ANNOVAR, converted from the vcf file. There is one output per sample.
  - `<sample_id>.avinput.variant_function`: ANNOVAR output, returning the position of a mutation on a gene.
  - `<sample_id>.avinput.exonic_variant_function`: ANNOVAR output, returning mutation effects on translation, namely synonymous, nonsynonymous, stop codon gain, or stop codon loss.
- Phylogenetic tree:
  - `core_genome_aln.tree`: A phylogenetic tree in newick format to estimate population structure effect for GWAS.
  - `phylogeny_distances.tsv`: A similarity matrix based on the phylogenetic distances between the samples (produced by the estimate_pop_structure module in MugGWAS). 
- MugGWAS output: `data/muggwas_output`
  - `gene_mutation_summary.txt`: This is a summary table documenting the mutation types for each gene across all samples (produced by the compile_variants_by_gene module in MugGWAS).
  -  `gene_annotation_summary.txt`: This documents the gene annotations from the gff3 file (produced by the compile_variants_by_gene module in MugGWAS).
  - `pyseer_results.txt`: This table documents the association results based on the mutation information by the pyseer GWAS pipeline (produced by the run_pyseer_COG module in MugGWAS).

