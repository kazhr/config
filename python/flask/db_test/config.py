#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
