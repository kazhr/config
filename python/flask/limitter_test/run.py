from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
)


@app.route("/slow")
@limiter.limit("1/minute")
def slow():
    return ":("


@app.route("/medium")
@limiter.limit("10/second")
def medium():
    return ":|"


@app.route("/fast")
def fast():
    return ":)"


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
