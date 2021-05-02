#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from utils.mymodule import get_cwd


@pytest.fixture(scope="function")
def cwd():

    return get_cwd()
