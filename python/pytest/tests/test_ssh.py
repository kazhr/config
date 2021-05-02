#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest


class TestSSH:

    def test_connect(self, ssh_client):
        assert ssh_client.is_ssh_available()

    def test_sudo(self, ssh_client):
        assert ssh_client.is_sudo_available()

    def test_sudo_privilege(self, ssh_client):
        assert ssh_client.get_sudo_privilege().endswith("NOPASSWD: ALL")
