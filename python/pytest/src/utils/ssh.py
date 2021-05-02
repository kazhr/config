#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import contextmanager
import paramiko


class SSHClient(object):
    """
    SSH

    Parameters
    ----------
    hostname : str

    username : str

    password : str

    port : int, optional
        default=22

    policy : "AutoAdd"|"Warging"|"Reject", optional
        新規ホストに接続するときの対応, default="AutoAdd"

    timeout : int, optional
        default=5

    Note
    ----
    単位時間あたりのssh回数制限に引っかかる可能性あり
    """

    def __init__(self, hostname, username, password,
                 ssh_port=22, policy="AutoAdd", timeout=5):

        policy = {
            "AutoAdd": paramiko.AutoAddPolicy(),
            "Warning": paramiko.WarningPolicy(),
            "Reject": paramiko.RejectPolicy(),
        }[policy]

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(policy)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_port = ssh_port
        self.timeout = timeout

    @contextmanager
    def connect(self):
        """
        Connect to the host
        """
        self.client.connect(
            hostname=self.hostname,
            port=self.ssh_port,
            username=self.username,
            password=self.password,
        )
        try:
            yield self.client
        finally:
            self.client.close()

    def exec_command(self, command):
        """
        execute a command on the remote host via ssh

        Parameters
        ----------
        commands : str

        Returns
        -------
        stdout : str
            including newline(s)

        stderr : str
            including newline(s)
        """
        with self.connect() as client:
            _, stdout, stderr = client.exec_command(command, self.timeout)
            stdout = stdout.read().decode().strip()
            stderr = stderr.read().decode().strip()
        return stdout, stderr

    def is_ssh_available(self):
        stdout, stderr = self.exec_command("whoami")
        return stdout == self.username

    def is_sudo_available(self):
        stdout, stderr = self.exec_command(f"echo {self.password}| sudo -S -l")
        return stdout != ""

    def get_sudo_privilege(self):
        stdout, stderr = self.exec_command(f"echo {self.password}| sudo -S -l")
        last_line = stdout.split("\n")[-1]
        return last_line.strip()
