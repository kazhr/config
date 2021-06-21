#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # noqa

root_url = "http://localhost:8888"
username = "test"
password = "password"


browser = os.getenv("BROWSER")
if browser is None:
    # use firefox as default
    browser = "firefox"
desired_capabilities = eval(f"DesiredCapabilities.{browser.upper()}")

with webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=desired_capabilities,
) as driver:

    url = urljoin(root_url, "login")
    driver.get(url)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("btn").click()
