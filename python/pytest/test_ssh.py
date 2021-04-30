#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.ssh import SSH
import pytest


# class SSHTestGroup(object):
#     """
#     Note
#     ----
#     単位時間あたりのssh回数制限に引っかかる可能性あり
#     """

#     def __init__(self, hostname, username, password, ssh_port):

#         self.client = SSH(hostname, username, password, ssh_port)
#         self.hostname = hostname
#         self.username = username
#         self.password = password
#         self.ssh_port = ssh_port

#     def is_ssh_available(self):
#         stdout, stderr = self.client.exec_command("whoami")
#         return stdout == self.username

#     def is_sudo_available(self):
#         stdout, stderr = self.client.exec_command(f"echo {self.password}| sudo -S -l")
#         return stdout != ""

#     def get_sudo_privilege(self):
#         stdout, stderr = self.client.exec_command(f"echo {self.password}| sudo -S -l")
#         last_line = stdout.split("\n")[-1]
#         return last_line.strip()


@pytest.fixture(scope="class")
def host():

    hostname = "localhost"
    username = "test"
    password = "password"
    ssh_port = 22
    ssh = SSH(hostname, username, password, ssh_port)

    return ssh


class TestSSH:

    def test_connect(self, host):
        assert host.is_ssh_available()

    def test_sudo(self, host):
        assert host.is_sudo_available()

    def test_sudo_privilege(self, host):
        assert host.get_sudo_privilege().endswith("NOPASSWD: ALL")
