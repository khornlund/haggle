#!/bin/bash

# teardown existing
./teardown-docker.sh

# build the flask container
docker build -t khornlund/haggle .

# create the network
docker network create haggle-net

# start the ES container
docker run -d --name es \
    --net haggle-net \
    -p 9200:9200 -p 9300:9300 \
    -e "discovery.type=single-node" \
    --rm \
    docker.elastic.co/elasticsearch/elasticsearch:7.1.0

# start the flask app container
docker run -d --name haggle\
    --net haggle-net \
    -p 5000:5000 \
    --rm \
    khornlund/haggle
