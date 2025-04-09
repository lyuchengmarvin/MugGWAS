#
# This is a Dockerfile for building a Docker image for the `MugGWAS` library.
#
# use a predefined image with conda 
FROM biocontainers/biocontainers:latest

# install dependencies, use exact versions for reproducibility
RUN conda config --add channels defaults \
    && conda config --add channels conda-forge \
    && conda config --add channels bioconda 
RUN conda install pyseer
RUN conda install python=3.9 \
    gffutils=0.13 \
    pandas=2.1.4  \
    biopython=1.81 \
    argh=0.26.2 \
    dendropy=5.0.6
# add the bash script
ADD ./run.py /scripts/run.py

WORKDIR /data

# here we could provide the desired default command
CMD ["pyseer"]