#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools


def result_decorator(func):
    """
    結果を見やすくするためのデコレータ
    """
    line_length = 25

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        print("")
        print("".center(line_length, "-"))
        func(*args, **kwargs)

    return wrapper
