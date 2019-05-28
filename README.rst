haggle
======

Flask web app for deploying NLP haggling model trained on Craigslist data.

Installation
------------
Use Anaconda to create and environment and install the necessary packages.

.. code:: bash

    conda create --name haggle python=3.6
    conda activate haggle
    conda install --file requirements.txt
    python setup.py develop

Usage
-----

Start Elasticsearch Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can start an Elasticsearch instance in a Docker container simply using:

.. code:: bash

    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.1.0

Start the Web App
~~~~~~~~~~~~~~~~~
With your conda environment activated:

.. code:: bash

    haggle webapp


Authors
-------
`haggle` was written by `Karl Hornlund <karlhornlund@gmail.com>`_.
