#!/bin/bash

git pull

./ipsec-router/build.sh

./webcrawler/build.sh

docker-compose up -d

docker-compose logs -f
