#!/bin/bash
set -eu

# 0: no, 1: yes
YUM_CRON=1
ADD_USER=0

function setup_yum_cron() {
  yum -y install yum-cron
  sed -i -e "s/apply_updates = no/apply_updates = yes/" /etc/yum/yum-cron.conf
  systemctl enable yum-cron
  systemctl start yum-cron
}

function setup_admin_user() {

  # username
  local user=""

  # password
  local pass=""

  # public key
  local pkey=""

  useradd -m -p $(openssl passwd -1 $pass) -s /bin/bash -G wheel $user

  # add public key
  mkdir -p /home/$user/.ssh
  echo "$pkey" >/home/$user/.ssh/authorized_keys

  # set owner & permissions
  chown $user. -R /home/$user/.ssh
  chmod 700 /home/$user/.ssh
}

# main
yum -y update
[ $YUM_CRON -eq 1 ] && setup_yum_cron
[ $ADD_USER -eq 1 ] && setup_admin_user
