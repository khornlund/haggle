FROM continuumio/miniconda3

# copy in the python webapp package, and create the conda environment
ADD flask-app/ /tmp/flask-app/
RUN conda env create --file /tmp/flask-app/environment.yml

# set shell to bash and activate the environment by default
SHELL ["/bin/bash", "-c"]
RUN echo "source activate haggle" > ~/.bashrc
ENV PATH /opt/conda/envs/haggle/bin:$PATH

EXPOSE 5000

# change to the root of the python package so relative paths will work
WORKDIR /tmp/flask-app/
ENTRYPOINT ["haggle", "webapp"]
