#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


def getenv(key):

    value = os.getenv(key)
    if value is None:
        emsg = f"E: not found {key} in env!"
        raise ValueError(emsg)

    return value
