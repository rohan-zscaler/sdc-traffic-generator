#!/usr/bin/env bash

echo Updating Configurations

echo ZSCALER_CLOUD	$ZSCALER_CLOUD 
echo VPN_USERNAME	$VPN_USERNAME 
echo VPN_ADDRESS	$VPN_ADDRESS
echo


envsubst '$VPN_USERNAME $VPN_PSK' < /etc/ipsec.secrets.tmpl > /etc/ipsec.secrets
envsubst '$ZSCALER_CLOUD $VPN_USERNAME $DOCKER_SUBNET $VPN_ADDRESS' < /etc/ipsec.conf.tmpl > /etc/ipsec.conf
