#!/usr/bin/env bash

ip route del default 
ip route add default via $DOCKER_VPN_GATEWAY_IP

echo "DOCKER_VPN_GATEWAY_IP: $DOCKER_VPN_GATEWAY_IP"

echo "nameserver $DNS1" >> /etc/resolv.conf
echo "nameserver $DNS2" >> /etc/resolv.conf

sleep 5

python3 /app/bootstrap.py
