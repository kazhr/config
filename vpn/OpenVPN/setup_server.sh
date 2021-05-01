#!/bin/bash
set -eu
[ $UID -ne 0 ] && echo "not root, bye." && exit 0

# setting
CLIENT_NAME=

# setup OpenVPN server
# (in ubuntu20)

# install
apt install openvpn easy-rsa

# initialize
EASY_RSA=/etc/openvpn/easy-rsa
mkdir $EASY_RSA
ln -s /usr/share/easy-rsa/* $EASY_RSA/
(cd $EASY_RSA && ./easyrsa init-pki)

# 認証局
cat <<EOT >$EASY_RSA/vars
set_var EASYRSA_REQ_COUNTRY    "JP"
set_var EASYRSA_REQ_PROVINCE   "."
set_var EASYRSA_REQ_CITY       ""
set_var EASYRSA_REQ_ORG        "."
set_var EASYRSA_REQ_EMAIL      "."
set_var EASYRSA_REQ_OU         "."
set_var EASYRSA_ALGO           "ec"
set_var EASYRSA_DIGEST         "sha512"
EOT
(cd $EASY_RSA && ./easyrsa build-ca nopass)

# サーバー証明書
(cd $EASY_RSA && ./easyrsa gen-req server nopass)
(cd $EASY_RSA && ./easyrsa sign-req server server)

cp $EASY_RSA/pki/ca.crt             /etc/openvpn/server/
cp $EASY_RSA/pki/issued/server.crt  /etc/openvpn/server/
cp $EASY_RSA/pki/private/server.key /etc/openvpn/server/

# 事前共有鍵
(cd $EASY_RSA && openvpn --genkey --secret ta.key)
cp $EASY_RSA/ta.key                /etc/openvpn/server/

# クライアント証明書
(cd $EASY_RSA && ./easyrsa gen-req $CLIENT_NAME nopass)
(cd $EASY_RSA && ./easyrsa sign-req client $CLIENT_NAME)

# OpenVPN
cat <<EOT >/etc/openvpn/server/server.conf
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh none
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist /var/log/openvpn/ipp.txt
push "redirect-gateway def1 bypass-dhcp"
keepalive 10 120
tls-crypt ta.key
cipher AES-256-GCM
auth SHA256
user nobody
group nogroup
persist-key
persist-tun
status /var/log/openvpn/openvpn-status.log
verb 3
explicit-exit-notify 1
EOT

# enable
systemctl enable openvpn-server@server.service
systemctl start openvpn-server@server.service
