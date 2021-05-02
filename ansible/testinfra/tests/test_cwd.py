#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_wd(host, cwd):

    print(host)
    print(cwd)

    assert not str(cwd) == "/"
