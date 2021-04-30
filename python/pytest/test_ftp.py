#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tempfile


class TestFTP:

    def test_transport_file(self, ftp_client):

        test_message = "This is a test message."
        remote_file = "test.txt"

        # check
        assert not ftp_client.exists(remote_file)

        try:
            # put test_message within a temp file
            with tempfile.NamedTemporaryFile(mode="w") as fp:
                fp.write(test_message)
                fp.seek(0)
                ftp_client.put(fp.name, remote_file)

            # get file and read
            with tempfile.NamedTemporaryFile(mode="r") as fp:
                ftp_client.get(remote_file, fp.name)
                received_message = fp.read()

            assert received_message == test_message

        finally:
            # remove the test file from remote
            ftp_client.delete(remote_file)

        assert not ftp_client.exists(remote_file)

    def test_directory(self, ftp_client):

        remote_dir = "test_dir"

        # check
        assert not ftp_client.exists(remote_dir)

        try:
            ftp_client.mkdir(remote_dir)
            assert ftp_client.is_dir(remote_dir)

            v = ftp_client.get_verbose(remote_dir)
            assert v["unix.mode"] == "0755"

        finally:
            ftp_client.rmdir(remote_dir)

        assert not ftp_client.exists(remote_dir)
