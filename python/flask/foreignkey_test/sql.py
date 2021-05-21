#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.confi["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

# create a db session
db = SQLAlchemy(app)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    notes = db.relationship("Note", backref="tag")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
