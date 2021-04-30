#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from utils.ftp import FTPClient
from utils.ssh import SSHClient


@pytest.fixture(scope="class")
def ssh_client():

    hostname = "localhost"
    username = "test"
    password = "password"
    ssh_port = 22
    ssh = SSHClient(hostname, username, password, ssh_port)

    return ssh


@pytest.fixture(scope="class")
def ftp_client():

    hostname = "localhost"
    username = "test"
    password = "password"
    ftp = FTPClient(hostname, username, password)

    return ftp
