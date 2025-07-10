#!/bin/bash

docker-compose up -d

./tail-logs.sh
