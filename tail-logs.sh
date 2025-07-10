#!/bin/bash

LINE_COUNT=200

if [[ $1 != "" ]]; then
  LINE_COUNT=$1
fi

docker-compose logs -f --tail=${LINE_COUNT}
