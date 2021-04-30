#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from utils.ftp import FTPClient


@pytest.fixture(scope="class")
def ftp_client():

    hostname = "localhost"
    username = "test"
    password = "password"
    ftp = FTPClient(hostname, username, password)

    return ftp
