# Expose key functions and classes from submodules
from .annotate_variants import run_annovar
from .compile_variants_by_gene import (
    GeneVariantAnalyzer,
    compile_gene_mutations,
    write_gene_mutation_summary,
    write_gene_annotation_summary
)
from .estimate_pop_structure import phylogeny2distmatrix
from .run_pyseer_COG import run_pyseer

# Define the package version
__version__ = "0.2.3"

__all__ = [
    "run_annovar",
    "GeneVariantAnalyzer",
    "compile_gene_mutations",
    "write_gene_mutation_summary",
    "write_gene_annotation_summary",
    "phylogeny2distmatrix",
    "run_pyseer"
]