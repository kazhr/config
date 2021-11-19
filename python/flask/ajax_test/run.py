#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax", methods=["POST"])
def show():

    name = request.form["name"]
    if name:
        msg = f"Hello! {request.form['name']}"
    else:
        msg = ""
    data = {
        "msg": msg
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
