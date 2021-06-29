#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # noqa


class SeleniumGrid:
    """
    how to switch browser:
    $ export BROWSER=crhome
    """
    def __init__(self):
        browser = os.getenv("BROWSER")
        if browser is None:
            # use firefox as default
            browser = "firefox"
        desired_capabilities = eval(f"DesiredCapabilities.{browser.upper()}")

        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=desired_capabilities,
        )

    def login(self, url, username, password):
        """
        demo to login
        """
        self.driver.get(url)
        self.driver.find_element_by_name("username").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_class_name("btn").click()


if __name__ == "__main__":
    sg = SeleniumGrid()
