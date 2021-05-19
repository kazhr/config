#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sql import app, db

if __name__ == "__main__":
    # テーブル作成
    db.create_all()

    # 起動
    app.run(
        host="127.0.0.1",
        port=8888,
        debug=True,
    )
