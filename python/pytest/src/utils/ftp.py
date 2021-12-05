#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import contextmanager
from ftplib import FTP
from pathlib import Path


class FTPClient(object):
    """
    FTP

    encoding : str, optional
        default="utf8"
    """

    def __init__(self, hostname, username, password,
                 timeout=5, encoding="utf8"):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        # python3.9ならデフォルトでutf8
        FTP.encoding = encoding

    @contextmanager
    def connect(self):

        client = FTP(
            host=self.hostname,
            user=self.username,
            passwd=self.password,
            timeout=self.timeout,
        )
        try:
            yield client
        finally:
            client.quit()

    def ls(self, remote_path):
        """
        Returns
        -------
        files : list
        """

        with self.connect() as client:
            files = client.nlst(remote_path)
        return files

    def get_verbose(self, remote_path):

        remote_path = Path(remote_path)

        with self.connect() as client:
            for (name, verbose) in client.mlsd(remote_path.parent):
                if name == remote_path.name:
                    return verbose
            else:
                emsg = "not found."
                raise ValueError(emsg)

    def exists(self, remote_path):
        try:
            self.get_verbose(remote_path)
            return True
        except ValueError:
            return False

    def is_dir(self, remote_path):

        verbose = self.get_verbose(remote_path)
        return verbose["type"] == "dir"

    def is_file(self, remote_path):

        verbose = self.get_verbose(remote_path)
        return verbose["type"] == "file"

    def mkdir(self, remote_path):

        with self.connect() as client:
            client.mkd(remote_path)

    def rmdir(self, remote_path):

        with self.connect() as client:
            client.rmd(remote_path)

    def put(self, local_src, remote_dest):
        """
        Parameters
        ----------
        src : str|Path
            local path

        dest : str
            remote path
        """

        if self.exists(remote_dest):
            emsg = f"{remote_dest} already exists!"
            raise ValueError(emsg)

        local_src = Path(local_src).expanduser()

        with self.connect() as client:
            with local_src.open("rb") as obj:
                client.storbinary(f"STOR {remote_dest}", obj)

    def get(self, remote_src, local_dest):

        local_dest = Path(local_dest).expanduser()

        with self.connect() as client:
            with local_dest.open("wb") as obj:
                client.retrbinary(f"RETR {remote_src}", obj.write)

    def delete(self, remote_path):

        with self.connect() as client:
            client.delete(remote_path)

    def cmd(self, cmd):

        with self.connect() as client:
            client.sendcmd(cmd)
