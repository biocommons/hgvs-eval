#!/bin/bash

# run swagger UI from docker container
# setup: install docker, instantiate hgvs server and express here.

# parameter: $1 = complete url of swagger json [http://192.168.99.100:8000/api]
if [ $# -eq 0 ]
  then
    echo "Please pass URL of HGVS swagger endpoint"
    exit 1;
fi

docker run -d --name swagger-ui -p 8888:8888 -e "API_URL=$1" sjeandeaux/docker-swagger-ui
