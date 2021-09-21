#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
import traceback


def something_wrong(e):
    if isinstance(e, HTTPException):
        return e, e.code

    emsg = "<pre>"
    for line in traceback.TracebackException.from_exception(e).format():
        emsg += line
    emsg += "</pre>"
    return emsg, 500


app = Flask(__name__)
app.register_error_handler(Exception, something_wrong)


@app.route("/")
def index():
    data = {
        "state": "OK"
    }
    return jsonify(data)


@app.route("/int/<n>/")
def test(n):
    x = 1/int(n)
    data = {
        "result": x,
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
