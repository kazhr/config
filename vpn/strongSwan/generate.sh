#!/bin/bash
set -eu
[ $UID -ne 0 ] && echo "not root, bye." && exit 0

CN=
CLIENT_NAME=
CLIENT_PASS=
SUBNET='10.16.0.0/24'
DNS='8.8.8.8,8.8.4.4'

function install() {
  # Debian 10
  apt install strongswan strongswan-pki libcharon-extra-plugins
}

function generate_ca_key() {
  # 4096ビットの RSA 秘密鍵
  ipsec pki \
    --gen \
    --type rsa \
    --size 4096 \
    --outform pem \
    > ./ca-key.pem
  chmod 600 ca-key.pem
}

function generate_ca_cert() {
  # 自己署名ルート CA 証明書
  #   - 有効期限: 10年間(3650日)
  ipsec pki \
    --self \
    --ca \
    --lifetime 3650 \
    --in ./ca-key.pem \
    --type rsa \
    --dn "C=JP, O=strongSwan, CN=strongSwan Root CA" \
    --outform pem \
    > ./ca-cert.pem
}

function generate_server_key() {
  # 2048ビットの RSA 秘密鍵
  ipsec pki \
    --gen \
    --type rsa \
    --size 2048 \
    --outform pem \
    > ./server-key.pem
  chmod 600 server-key.pem
}

function generate_server_cert() {
  # ホスト証明書
  #   - 有効期限: 5年(1825日)
  ipsec pki --pub --in ./server-key.pem --type rsa| \
    ipsec pki \
      --issue --lifetime 1825 \
      --cacert ./ca-cert.pem \
      --cakey ./ca-key.pem \
      --dn "C=JP, O=strongSwan, CN=$CN" \
      --san "$CN" \
      --flag serverAuth --flag ikeIntermediate \
      --outform pem \
    > ./server-cert.pem
}

function generate_client_key() {
  ipsec pki \
    --gen \
    --type rsa \
    --size 2048 \
    --outform pem \
    > ./client-key.pem
  chmod 600 ./client-key.pem
}

function generate_client_cert() {
  local mail="${CLIENT_NAME}@${CN}"
  ipsec pki --pub --in ./client-key.pem --type rsa | \
    ipsec pki \
      --issue --lifetime 1825 \
      --cacert ./ca-cert.pem \
      --cakey ./ca-key.pem \
      --dn "C=JP, O=strongSwan, CN=${mail}" \
      --san "${mail}" \
      --outform pem \
    > ./client-cert.pem

  openssl pkcs12 \
    -export \
    -inkey client-key.pem \
    -in client-cert.pem \
    -name "VPN client certificate" \
    -certfile ca-cert.pem \
    -caname "strongSwan Root CA" \
    -out client.p12
}

function generate_secret() {
cat <<EOT >/etc/ipsec.secret
# This file holds shared secrets or RSA private keys for authentication.

# RSA private key for this host, authenticating it to any other host
# which knows the public part.
: RSA server-key.pem

# this file is managed with debconf and will contain the automatically created private key
include /var/lib/strongswan/ipsec.secrets.inc

$CLIENT_NMAE : EAP "$CLIENT_PASS"
EOT
}

function generate_conf() {
cat <<EOT > /etc/ipsec.conf
# ipsec.conf - strongSwan IPsec configuration file

# basic configuration
config setup
  #uniqueids=never
  charondebug="ike 2, knl 2, cfg 2, net 2, esp 2, dmn 2, mgr 2"

conn %default
  keyexchange=ikev2

  # Prefer modern cipher suites that allow PFS (Perfect Forward Secrecy)
  ike=aes128-sha256-ecp256,aes256-sha384-ecp384,aes128-sha256-modp2048,aes128-sha1-modp2048,aes256-sha384-modp4096,aes256-sha256-modp4096,aes256-sha1-modp4096,aes128-sha256-modp1536,aes128-sha1-modp1536,aes256-sha384-modp2048,aes256-sha256-modp2048,aes256-sha1-modp2048,aes128-sha256-modp1024,aes128-sha1-modp1024,aes256-sha384-modp1536,aes256-sha256-modp1536,aes256-sha1-modp1536,aes256-sha384-modp1024,aes256-sha256-modp1024,aes256-sha1-modp1024!
  esp=aes128gcm16-ecp256,aes256gcm16-ecp384,aes128-sha256-ecp256,aes256-sha384-ecp384,aes128-sha256-modp2048,aes128-sha1-modp2048,aes256-sha384-modp4096,aes256-sha256-modp4096,aes256-sha1-modp4096,aes128-sha256-modp1536,aes128-sha1-modp1536,aes256-sha384-modp2048,aes256-sha256-modp2048,aes256-sha1-modp2048,aes128-sha256-modp1024,aes128-sha1-modp1024,aes256-sha384-modp1536,aes256-sha256-modp1536,aes256-sha1-modp1536,aes256-sha384-modp1024,aes256-sha256-modp1024,aes256-sha1-modp1024,aes128gcm16,aes256gcm16,aes128-sha256,aes128-sha1,aes256-sha384,aes256-sha256,aes256-sha1!

  forceencaps=yes
  dpdaction=clear
  dpddelay=300s
  rekey=no

conn ipsec-ikev2-vpn
  auto=add

  left=%any
  leftsubnet=0.0.0.0/0
  leftcert=server-cert.pem
  leftid=@${CN}
  leftsendcert=always

  right=%any
  rightsourceip=${SUBNET}
  rightauth=eap-mschapv2
  rightdns=${DNS}

  # Windows対応
  eap_identity=%any

include /var/lib/strongswan/ipsec.conf.inc
EOT
}
