#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TestApache:

    def test_apache_is_installed(self, host):
        package = host.package("httpd")
        assert package.is_installed

    def test_apache_is_running(self, host):
        service = host.service("httpd")
        assert service.is_running
        assert service.is_enabled
