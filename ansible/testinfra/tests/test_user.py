#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_ansible_user(host):

    assert host.check_output("whoami") == "developer"
