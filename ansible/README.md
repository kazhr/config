# 事前準備
- パーミッション確認
```
$ chmod 400 ./centos/id_ed25519
```

- テスト用のホスト起動
```
# docker-compose up -d
```

- 接続テスト
```
$ ansible-playbook playbook/debug.yml
```
