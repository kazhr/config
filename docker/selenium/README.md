# Selenium
- 起動
```
$ docker-compose up (-d)
```

# firefoxを使用
## 操作状況確認(noVNC) / 手動操作
- localhost:7902(->7900)に接続
  - 初期パスワード: secret

## pythonから操作
- 起動
```
$ ipython
In [1]: %run ./selenium_browser.py
```

- ブラウズ
```
In [2]: sg.driver.get("https://google.com")
```
