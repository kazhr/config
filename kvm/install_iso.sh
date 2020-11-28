#!/bin/bash
set -eu

INSTALL_DIR=
ISO_FILE=
if [ ! -e $ISO_FILE ]; then
  echo "not found $ISO_FILE!"
  exit 1
fi

NAME=
SIZE=16G
RAM=4096
CPU=1
BRIDGE=br0


function _create_img() {
  if [ ! -e $INSTALL_DIR ]; then
    mkdir -p $INSTALL_DIR
  fi

  disk_img=$INSTALL_DIR/${NAME}.img
  if [ -e $disk_img ]; then
    echo "$disk_img already exists!"
    return 1
  fi

  qemu-img create -f qcow2 ${disk_img} ${SIZE}
  echo ${disk_img}
}

virt-install \
  --name ${NAME} \
  --ram ${RAM} \
  --vcpus ${CPU} \
  --disk path=$(_create_img) \
  --os-type linux \
  --network bridge=${BRIDGE} \
  --graphics none \
  --location ${ISO_FILE} \
  --extra-args 'console=ttyS0,115200n8 serial'
