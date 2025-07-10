#!/usr/bin/env bash

export MYIP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
export DOCKER_SUBNET=$(ip -o -f inet addr show | awk '/scope global/ {print $4}')

echo
echo MYIP		$MYIP
echo DOCKER_SUBNET	$DOCKER_SUBNET
echo

DIR=/docker-entrypoint.d
if [[ -d "$DIR" ]]; then
  /bin/run-parts --exit-on-error --verbose --regex '\.sh$' "$DIR"
fi

exec "$@"
