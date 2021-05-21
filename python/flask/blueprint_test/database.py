#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    ユーザー管理テーブル

    Parameters
    ----------
    name : str (max: 80)
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<User {self.name!r}>"
