#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import abort, flash, request, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, SubmitField, StringField, validators
from is_safe_url import is_safe_url

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize
app = Flask(__name__)
app.config["SECRET_KEY"] = "change me!"

# create a db session
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# initialize login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# 未認証ユーザーのデフォルトリダイレクト先
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(pk):
    """
    UserMixin.get_id()を受け取ってLoginMangerへ渡す
    """
    return User.query.get(int(pk))


class User(db.Model, UserMixin):
    """
    一般ユーザー管理

    Parameters
    ----------
    username : str (max: 80)

    mailaddr : str (max: 120)

    password : str (max: 120)
        ハッシュ化されたパスワード
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    mailaddr = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, username, mailaddr, password):
        self.username = username
        self.mailaddr = mailaddr
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.username!r}>"


class EmailForm(FlaskForm):
    """
    メールアドレス入力用フォーム
    """
    mailaddr = StringField(
        "Emailアドレス",
        [
            validators.Required(),
            validators.Email(check_deliverability=True, message="有効なメールアドレスを入力してください!"),
        ],
    )


class PasswordForm(FlaskForm):
    """
    パスワード入力用フォーム
    """
    password = PasswordField(
        label="パスワード",
        validators=[
            validators.DataRequired(),
            validators.Length(min=8, max=32, message='8文字以上32文字以内で入力!'),
            # validators.Regexp('(?=.*?[A-Z])', message="一文字以上の大文字を含めてください!"),
            # validators.Regexp('(?=.*?[0-9])', message="一文字以上の数字を含めてください!"),
            # validators.Regexp('(?=.*?[#?!@$%^&*-])', message="一文字以上の記号を含めてください!(使用できる記号: #?!@$%^&*-)"),
            validators.EqualTo('confirm', message="パスワードが一致しません!"),
        ],
    )
    confirm = PasswordField(
        label="パスワード再入力",
        validators=[
            validators.DataRequired(),
        ],
    )


@app.route('/')
def index():
    return render_template("index.html")


class CreateForm(EmailForm, PasswordForm):
    """
    新規ユーザー登録用フォーム
    """
    username = StringField(
        "ユーザー名",
        [
            validators.Required(),
            validators.Length(min=4, message='4文字以上で入力してください!'),
        ],
    )
    submit = SubmitField("登録")


@app.route("/create", methods=["GET", "POST"])
def create():
    """
    新規ユーザー登録
    """
    form = CreateForm(request.form)
    if form.validate_on_submit():

        username = form.username.data
        mailaddr = form.mailaddr.data
        # password = generate_password_hash(form.password.data)
        password = form.password.data

        # check
        if User.query.filter_by(username=username).first() is not None:
            emsg = f"{username}はすでに使われています!!"
            flash(emsg)
            return redirect(url_for("create"))

        user = User(username, mailaddr, password)
        # update db
        db.session.add(user)
        db.session.commit()

        flash("登録に成功しました!")
        return redirect(url_for("login"))

    # GET
    return render_template("create.html", form=form)


class LoginForm(FlaskForm):
    """
    ユーザーログイン用フォーム
    """
    username = StringField("ユーザー名")
    password = PasswordField("パスワード")
    submit = SubmitField("ログイン")


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    ユーザーログイン
    """
    form = LoginForm(request.form)
    if form.validate_on_submit():

        username = form.username.data
        user = User.query.filter_by(username=username).first()

        if user is None:
            emsg = "ユーザー名が存在しません!"
            flash(emsg)
            return redirect(url_for("login"))

        if not check_password_hash(user.password, form.password.data):
            emsg = "パスワードが一致しません!"
            flash(emsg)
            return redirect(url_for("login"))

        login_user(user, remember=True)
        flash("Logged in successfully.")

        next = request.args.get("next")
        if next is not None and not is_safe_url(next, None):
            return abort(400)

        return redirect(next or url_for("index"))

    # GET
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    """
    ログアウト
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/user")
@login_required
def detail():
    """
    ユーザー情報詳細表示
    """
    user = User.query.get(current_user.id)
    return render_template("detail.html", user=user)


class UpdateEmailForm(EmailForm):
    """
    メールアドレス更新用フォーム
    """
    submit = SubmitField("更新")


@app.route("/user/update/email", methods=["GET", "POST"])
@login_required
def update_email():
    """
    メールアドレス更新
    """
    user = User.query.get(current_user.id)
    form = UpdateEmailForm(request.form)

    if form.validate_on_submit():

        user.mailaddr = form.mailaddr.data
        # update db
        db.session.add(user)
        db.session.commit()

        flash("メールアドレスを更新しました!")
        return redirect(url_for("detail"))

    return render_template("update_email.html", user=user, form=form)


class UpdatePasswordForm(PasswordForm):
    """
    パスワード更新用フォーム
    """
    current_password = PasswordField("現在のパスワード")
    submit = SubmitField("更新")


@app.route("/user/update/password", methods=["GET", "POST"])
@login_required
def update_password():
    """
    パスワード更新
    """
    user = User.query.get(current_user.id)
    form = UpdatePasswordForm(request.form)

    if form.validate_on_submit():

        if not check_password_hash(user.password, form.current_password.data):
            emsg = "現在のパスワードが正しくありません!"
            flash(emsg)
            return redirect(url_for("update_password"))

        user.password = generate_password_hash(form.password.data)
        # update db
        db.session.add(user)
        db.session.commit()

        flash("パスワードを更新しました!")
        return redirect(url_for("detail"))

    return render_template("update_password.html", user=user, form=form)
