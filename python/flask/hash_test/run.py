from flask import flash, Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "change me!"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("input.html")

    password = request.form["password"]
    hashed_pass = generate_password_hash(password)
    return redirect(url_for("check", hashed_pass=hashed_pass))


@app.route("/<hashed_pass>", methods=["GET", "POST"])
def check(hashed_pass):
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
