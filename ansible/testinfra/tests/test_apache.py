#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


class Package:
    package_name = "httpd"

    def test_package_is_installed(self, host):
        package = host.package(self.package_name)
        assert package.is_installed


class Service:
    service_name = "httpd"

    def test_service_is_running(self, host):
        service = host.service(self.service_name)
        assert service.is_running
        assert service.is_enabled


class TestApache(Package, Service):

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
