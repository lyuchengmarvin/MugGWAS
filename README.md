# **Mutated-gene Genome-Wide Association Study (MugGWAS)**

MugGWAS offers an non-model-organism-friendly pipeline to infer gene-trait association. It tackles common challenges faced by non-model organism research—such as lack of readily available annotation databases and small sample sizes—by integrating a simple annotation pipeline with mutation-centric GWAS analysis. Users can identify putative gene mutations that drive phenotypic change without the large statistical power required to perform genome-wide tests on a per-nucleotide basis.

## Motivation

Understanding the genetic basis of a trait is central to much biological research that helps gain mechanistic insight into complex biological phenomena. For instance, the discovery of genetic loci that contribute to antibiotic resistance could better our knowledge of how important pathogens evolve to escape medicinal application. 

Most association tools classify raw genetic variants (like single nucleotide polymorphisms or structural variants) into reference or alternative genotypes and then perform statistical tests to infer associations between particular variants and phenotypes. However, genome-wide analyses typically require large sample sizes for statistical power—a major challenge for organisms that are difficult to culture or traits that are challenging to measure. Alternative approaches test associations between phenotypes and gene presence/absence, but these methods don't capture finer details like important mutations that potentially disrupt gene function.

Mutated-gene Genome-Wide Association Study (MugGWAS) addresses these limitations by offering a non-model-organism-friendly pipeline to infer gene-trait associations. By annotating disruptive mutation types (nonsense, missense, stopgain, or nonstop), MugGWAS identifies putative gene dysfunctions associated with phenotypic changes. This approach conserves statistical power by avoiding tests on variants that either (1) don't affect function at the gene level or (2) result in disruption of the same gene, allowing users to identify putative gene mutations driving phenotypic changes without the large statistical power required for per-nucleotide genome-wide tests.

## Key Features

**Annotate the variants:**
- External tool: ANNOVAR, users need to [download](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) this themselves.
- Functionality: Annotate the variants for each sample to infer their mutation types on a gene. Compile these mutations gene by gene.

**Build gene mutation table:**
- Functionality: 
  1. Determine the mutation types for each gene across all samples. Users can specify if they want to output 'binary genotypes', i.e. mutated or wildtype, or 'multiple genotypes', i.e. nonsense, nonstop, missense, silent, or wildtype. MugGWAS now uses a binary classification (mutant or wildtype) for GWAS.
  2. Output a gene annotation table for the users' reference.

**Estimate the population structure effect:**
- Functionality: Infer population structure based on phylogenetic distances. Since MugGWAS will use a linear mixed model, the distance will be estimated from the shared branch length between the MRCA and the root.

**Run GWAS through Pyseer:**
- Functionality: Run mixed effect model from `Pyseer` to infer gene-trait association.

## Installation

#### Dependencies
MugGWAS uses ANNOVAR to annotate the variants. Please follow the [instructions](http://annovar.openbioinformatics.org/en/latest/) to download **ANNOVAR** (_registration is required_), and specify the path to ANNOVAR scripts for MugGWAS. More instructions are provided below.

#### Build Conda Environment

Download the [environmental.yaml](https://github.com/lyuchengmarvin/MugGWAS/blob/main/envs/environment.yaml) file for setting up your conda environement. You can download it using this command in your terminal.

```{command line}
wget https://github.com/lyuchengmarvin/MugGWAS/blob/main/envs/environment.yaml 
```

Build the environment to satisfy software prerequisites and ensure applicability.

```{command line}
conda env create --name muggwas --file envs/environment.yaml
```

Activate envrionment before use each time:

```{command line}
conda activate muggwas
```

Deactivate after use:

```{command line}
conda deactivate
```

#### Install MugGWAS

Install MugGWAS in your environment and make sure that all prerequisites are fulfilled.

```{command line}
pip install -i https://test.pypi.org/simple/ MugGWAS
```

## Data requirements

#### Input:
  - **snp.vcf.gz**: A vcf file (gzip is supported) containing single nucleotide variants of the samples. This should be called based on the reference genome.
  - **ref.fna**: A fasta file for the nucleotide sequence of the reference genome assembly.
  - **ref.gff3**: A gff3 file for the gene annotation of the reference genome.
  - **tree.nwk**: A phylogenetic tree in newick format inferred from the core genes of the samples.

#### MugGWAS Output:
  - **Gene mutation summary table**: a summary table documenting the mutation types for each gene across all samples. MugGWAS now uses a binary classification (mutant or wildtype) for GWAS but users can request for detailed information, i.e. nonsense, nonstop, missense, silent or wildtype, by specifying a 'multiple' model.
  - **Gene annotation summary table**: This documents the gene annotations from the gff3 file.
  - **GWAS statistical restult**: a table documenting the association results based on the mutation information by the pyseer GWAS pipeline.

## Usage

The functions will be readily available in your python environment once you import muggwas. Read this [tutorial](https://github.com/lyuchengmarvin/MugGWAS/blob/main/tutorials/tutorial.ipynb) for full implemetation of the MugGWAS pipeline.


## Citation

If you use MugGWAS for your research please cite:

```
Lin, Y.C.M. Mutated-gene Genome-Wide Association Study (MugGWAS). [Software]. (2025). Available from: https://github.com/lyuchengmarvin/MugGWAS
```

MugGWAS is a gene-trait association pipeline that integrates the annotation tool-**ANNOVAR** and the GWAS tool-**pyseer**. If you use these two tools together with MugGWAS, please cite:

```
Wang, K., Li, M., Hakonarson, H. ANNOVAR: Functional annotation of genetic variants from next-generation sequencing data. Nucleic Acids Research 38:e164 (2010).

Lees, J.A., Galardini, M., Bentley, S.D. et al. Pyseer: a comprehensive tool for microbial pangenome-wide association studies. Bioinformatics 34(24): 4310–4312 (2018).
```
## License

MugGWAS is available under the MIT License. See the LICENSE file for details.
