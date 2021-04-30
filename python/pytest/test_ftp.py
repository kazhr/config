#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import tempfile
from utils.ftp import FTPClient


@pytest.fixture(scope="class")
def client():

    hostname = "localhost"
    username = "test"
    password = "password"
    ftp = FTPClient(hostname, username, password)

    return ftp


class TestFTP:

    def test_transport_file(self, client):

        test_message = "This is a test message."
        remote_file = "test.txt"

        # check
        assert not client.exists(remote_file)

        try:
            # put test_message within a temp file
            with tempfile.NamedTemporaryFile(mode="w") as fp:
                fp.write(test_message)
                fp.seek(0)
                client.put(fp.name, remote_file)

            # get file and read
            with tempfile.NamedTemporaryFile(mode="r") as fp:
                client.get(remote_file, fp.name)
                received_message = fp.read()

            assert received_message == test_message

        finally:
            # remove the test file from remote
            client.delete(remote_file)

        assert not client.exists(remote_file)

    def test_directory(self, client):

        remote_dir = "test_dir"

        # check
        assert not client.exists(remote_dir)

        try:
            client.mkdir(remote_dir)
            assert client.is_dir(remote_dir)

            v = client.get_verbose(remote_dir)
            assert v["unix.mode"] == "0755"

        finally:
            client.rmdir(remote_dir)

        assert not client.exists(remote_dir)
