#!/usr/bin/env bash

sysctl net.ipv4.conf.all.send_redirects=1
sysctl net.ipv4.conf.default.send_redirects=1

sysctl net.ipv4.ip_forward=1
sysctl net.ipv6.conf.all.forwarding=1

#ip xfrm policy add src $MYIP/32 dst $DOCKER_SUBNET dir out priority 100
#ip xfrm policy add src $DOCKER_SUBNET dst $MYIP/32 dir in priority 100
