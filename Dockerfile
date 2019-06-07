FROM continuumio/miniconda3

# allow access to environment file
ADD flask-app/ /tmp/flask-app/
RUN conda env create --file /tmp/flask-app/environment.yml

# set shell to bash
SHELL ["/bin/bash", "-c"]

RUN echo "source activate haggle" > ~/.bashrc
ENV PATH /opt/conda/envs/haggle/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["haggle", "webapp"]
