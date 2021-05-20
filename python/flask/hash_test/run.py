from flask import flash, Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, validators

app = Flask(__name__)
app.config["SECRET_KEY"] = "change me!"


class PasswordForm(FlaskForm):
    """
    パスワード入力用のForm
    """
    password = PasswordField(
        label="password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=8, max=32, message='8文字以上32文字以内で入力!'),
            validators.Regexp('(?=.*?[A-Z])', message="一文字以上の大文字を含めてください!"),
            validators.Regexp('(?=.*?[0-9])', message="一文字以上の数字を含めてください!"),
            validators.Regexp('(?=.*?[#?!@$%^&*-])', message="一文字以上の記号を含めてください!(使用できる記号: #?!@$%^&*-)"),
        ],
    )


@app.route("/", methods=["GET", "POST"])
def index():
    """
    パスワード入力
    """
    form = PasswordForm(request.form)
    if form.validate_on_submit():

        password = form.password.data
        hashed_pass = generate_password_hash(password)
        return redirect(url_for("check", hashed_pass=hashed_pass))

    return render_template("input.html", form=form)


@app.route("/<hashed_pass>", methods=["GET", "POST"])
def check(hashed_pass):
    """
    ハッシュ化されたパスワードと一致するか
    """
    if request.method == "GET":
        return render_template("check.html", hashed_pass=hashed_pass)

    password = request.form["password"]
    if check_password_hash(hashed_pass, password):
        msg = "The same password!"
    else:
        msg = "wrong password"

    flash(msg)
    return redirect(url_for("check", hashed_pass=hashed_pass))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
