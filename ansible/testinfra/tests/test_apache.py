#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


class TestApache:

    def test_apache_is_installed(self, host):
        package = host.package("httpd")
        assert package.is_installed

    def test_apache_is_running(self, host):
        service = host.service("httpd")
        assert service.is_running
        assert service.is_enabled

    def test_apache_test_page(self, host):
        hostname = host.backend.hostname
        ansible_variables = host.backend.ansible_runner.get_variables(hostname)
        ansible_host = ansible_variables["ansible_host"]
        url = f"http://{ansible_host}"

        res = requests.get(url)
        assert res.status_code == 403

        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find("title").text
        assert title == "Apache HTTP Server Test Page powered by CentOS"
