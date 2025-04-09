from setuptools import setup, find_packages

setup(
    name="MugGWAS",
    version="0.1.0",
    author="Yu-Cheng Lin",
    description="A pipeline for GWAS analysis using phylogeny and gene mutations.",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Include all files in the data folder and optionally the scripts if needed
        "MugGWAS": ["data/*", "design_documents/*","scripts/*", "tutorials/*"],
    },
    install_requires=[
        "pandas==2.1.4",
        "dendropy",
        "biopython==1.81",
        "gffutils==0.13",
        "argh",
        "setuptools"
    ],
)
