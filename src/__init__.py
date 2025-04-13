# Expose key functions and classes from submodules
from .scripts.annotate_variants import run_annovar
from .scripts.compile_variants_by_gene import (
    GeneVariantAnalyzer,
    compile_gene_mutations,
    write_gene_mutation_summary,
)
from .scripts.estimate_pop_structure import phylogeny2distmatrix

# Define the package version
__version__ = "0.1.0"