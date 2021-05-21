#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import flash, request, render_template, redirect, url_for
from flask import Blueprint
from database import db, User

view = Blueprint("view", __name__)


@view.route("/")
def index():
    """
    一覧表示
    """
    users = User.query.all()
    return render_template("index.html", users=users)


@view.route("/create", methods=["GET", "POST"])
def create():
    """
    新規作成
    """
    if request.method == "GET":
        # create用pageを表示
        return render_template("create.html")

    name = request.form["name"]

    # check
    if User.query.filter_by(name=name).first() is not None:
        flash(f"{name} already exists!")
        return redirect(url_for("view.create"))

    # add
    user = User(name)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("view.index"))
