#!/usr/bin/env bash

case "$PLUTO_VERB:$1" in
up-client:)
#  iptables -t mangle -A INPUT -i $PLUTO_INTERFACE -s $PLUTO_PEER_CLIENT -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
#  iptables -t mangle -A OUTPUT -o $PLUTO_INTERFACE -d $PLUTO_PEER_CLIENT -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
  ;;
down-client:)
#  iptables -t mangle -D INPUT -i $PLUTO_INTERFACE -s $PLUTO_PEER_CLIENT -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
#  iptables -t mangle -D OUTPUT -o $PLUTO_INTERFACE -d $PLUTO_PEER_CLIENT -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
  ;;
esac
