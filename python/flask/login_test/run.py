#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import abort, flash, Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from is_safe_url import is_safe_url


# initialize
app = Flask(__name__)
app.config["SECRET_KEY"] = "change me!"

login_manager = LoginManager()
login_manager.init_app(app)

# 未認証ユーザーのデフォルトリダイレクト先
login_manager.login_view = "login"
# リダイレクト先として許可するホスト
allowed_hosts = []
# allowed_hosts = ["localhost"]


class User(UserMixin):
    """
    ログインユーザーを管理するモデル
    (とりあえずdbなしでテスト)
    user_loaderのためにself.idは必須

    Parameters
    ----------
    pk : int
        primary_keyの代わり

    username : str
    """
    def __init__(self, pk, username):
        self.id = pk
        self.username = username


# dbを使わないので直打ちでダミーを用意
users = {
    "1": User(1, "test"),
    "2": User(2, "hoge"),
}


@login_manager.user_loader
def load_user(pk):
    """
    UserMixin.get_id()を受け取る
    """
    return users[pk]
    # return User.query.get(pk)


@app.route('/')
def index():
    return render_template("index.html")


class LoginForm(FlaskForm):
    """
    Login用Formの作成
    """

    username = StringField(
        "username",
        [
            validators.Required(),
        ],
    )


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    ログイン
    """
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # ダミーからusernameが一致するデータを無理やり探してくる
            user = [user for pk, user in users.items() if user.username == form.username.data][0]

        except IndexError:
            flash(f"{form.username.data} does not exist!")
            return redirect(url_for("login"))

        login_user(user)
        flash("Logged in successfully.")

        next = request.args.get("next")
        if not is_safe_url(next, allowed_hosts):
            return abort(400)

        return redirect(next or url_for("index"))

    # get
    return render_template("login.html", form=form)


@app.route("/protected")
@login_required
def protected():
    """
    要ログインページ
    """
    return render_template("protected.html")


@app.route('/logout')
@login_required
def logout():
    """
    ログアウト
    """
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
