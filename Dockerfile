FROM continuumio/miniconda3

# allow access to environment file
ADD flask-app/ /tmp/flask-app/
RUN conda env create --file /tmp/flask-app/environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/flask-app/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/flask-app/environment.yml | cut -d' ' -f2)/bin:$PATH

EXPOSE 5000

CMD ["haggle", "webapp"]
