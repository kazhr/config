#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import flash, Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create a db session
db = SQLAlchemy()


class User(db.Model):
    """
    ユーザーごとのメールアドレスを管理するモデル

    Parameters
    ----------
    username : str (max: 80)

    mailaddr : str (max: 120)
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    mailaddr = db.Column(db.String(120))

    def __init__(self, username, mailaddr):
        self.username = username
        self.mailaddr = mailaddr

    def __repr__(self):
        return f"<User {self.username!r}>"


def create_app():

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    @app.route("/")
    def index():
        """
        一覧表示
        """
        users = User.query.all()
        return render_template("index.html", users=users)

    @app.route("/create", methods=["GET", "POST"])
    def create():
        """
        新規作成
        """
        if request.method == "GET":
            # create用pageを表示
            return render_template("create.html")

        username = request.form["username"]
        mailaddr = request.form["mailaddr"]

        # check
        if User.query.filter_by(username=username).first() is not None:
            flash(f"{username} already exists!")
            return redirect(url_for("create"))

        # add
        user = User(username, mailaddr)

        # update db
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("detail", pk=user.id))

    @app.route("/user/<pk>")
    def detail(pk):
        """
        個別詳細表示
        """
        user = User.query.get(pk)
        return render_template("detail.html", user=user)

    @app.route("/user/<pk>/update", methods=["GET", "POST"])
    def update(pk):
        """
        メールアドレス更新
        """
        user = User.query.get(pk)

        if request.method == "GET":
            # update用pageを表示
            return render_template("update.html", user=user)

        user.mailaddr = request.form["new_mailaddr"]

        # update db
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("detail", pk=user.id))

    @app.route("/user/<pk>/delete", methods=["GET", "POST"])
    def delete(pk):
        """
        ユーザー情報を削除
        """
        user = User.query.get(pk)

        if request.method == "GET":
            # 確認用pageを表示
            return render_template("confirm.html", user=user)

        # update db
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("index"))

    return app
