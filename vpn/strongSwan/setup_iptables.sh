#!/bin/bash
set -eu
[ $UID -ne 0 ] && echo "not root, bye." && exit 0

# global NIC
readonly GLOBAL=""

# strongswanのIPレンジ
SUBNET=$(cat /etc/ipsec.conf| grep -v "#"| grep rightsourceip| awk -F= '{print $2}')

iptables -N STRONGSWAN_INPUT
iptables -F STRONGSWAN_INPUT
iptables -A STRONGSWAN_INPUT -p esp -j ACCEPT
iptables -A STRONGSWAN_INPUT -p udp --dport 500 -j ACCEPT
iptables -A STRONGSWAN_INPUT -p udp --dport 4500 -j ACCEPT
iptables -A STRONGSWAN_INPUT -j RETURN
#iptables -I INPUT ${input_rulenum} -j STRONGSWAN_INPUT

iptables -N STRONGSWAN_FORWARD
iptables -F STRONGSWAN_FORWARD
iptables -A STRONGSWAN_FORWARD --match policy --pol ipsec --dir in -s $SUBNET --proto esp -j ACCEPT
iptables -A STRONGSWAN_FORWARD --match policy --pol ipsec --dir out -d $SUBNET --proto esp -j ACCEPT
iptables -A STRONGSWAN_FORWARD --match policy --pol ipsec --dir in -s $SUBNET -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
iptables -A STRONGSWAN_FORWARD --match policy --pol ipsec --dir out -d $SUBNET -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360
iptables -A STRONGSWAN_FORWARD -j RETURN
#iptables -I FORWARD ${forward_rulenum} -j STRONGSWAN_FORWARD

iptables -t nat -N STRONGSWAN
iptables -t nat -F STRONGSWAN
iptables -t nat -A STRONGSWAN -s $SUBNET -o $GLOBAL -m policy --pol ipsec --dir out -j ACCEPT
iptables -t nat -A STRONGSWAN -s $SUBNET -o $GLOBAL -j MASQUERADE
iptables -t nat -A STRONGSWAN -j RETURN
# iptables -t nat -I POSTROUTING ${postrouting_rulenum} -j STRONGSWAN
