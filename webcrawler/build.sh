#!/bin/bash

git pull

current_dir=$(pwd)
script_dir=$(dirname $0)

if [ $script_dir = '.' ]
then
  script_dir="$current_dir"
elif [[ $script_dir != /* ]]
then
  script_dir="$current_dir/$script_dir"
fi

IMAGE_NAME=webcrawler

docker build -t ${IMAGE_NAME}:latest -f $script_dir/Dockerfile $script_dir

