# Expose key functions and classes from submodules
from .annotate_variants import run_annovar
from .compile_variants_by_gene import (
    GeneVariantAnalyzer,
    compile_gene_mutations,
    write_gene_mutation_summary,
)
from .estimate_pop_structure import phylogeny2distmatrix

# Define the package version
__version__ = "0.2.2"

__all__ = [
    "run_annovar",
    "GeneVariantAnalyzer",
    "compile_gene_mutations",
    "write_gene_mutation_summary",
    "phylogeny2distmatrix"
]