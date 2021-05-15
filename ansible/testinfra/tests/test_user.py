#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UserTest:
    username = None
    def test_ansible_user(self, host):
        assert host.check_output("whoami") == self.username


class TestDeveloperUser(UserTest):
    username = "developer"
