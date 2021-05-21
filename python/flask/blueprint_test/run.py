#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database import db
from flask import Flask
from views import view


if __name__ == "__main__":

    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(view)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 起動
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
