from setuptools import setup, find_packages

setup(
    name="MugGWAS",
    version="0.1.0",
    author="Yu-Cheng Lin",
    description="A pipeline for GWAS analysis using phylogeny and gene mutations.",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "dendropy",
        "gffutils",
        "setuptools"
    ],
)
