#!/bin/bash

# This script is a way to run stop and stop commands on docker-compose managed containers

if [ $# -lt 2 ]; then
	echo "ERROR: two args required!"
	echo "Usage: dc-action.sh <action:start|stop> <container>"
	exit 1 
fi

date

#echo "action: $1; container: $2" 

cd /home/ec2-user/sdc-traffic-generator/

/usr/local/bin/docker-compose $1 $2
