#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 接続
client.connect(
    hostname="localhost",
    username="test",
    password="password",
    port=10022,
)

# ttyありでcmd実行
cmd = "sudo whoami"
stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)

print("buffer size: ", len(stdout.channel.in_buffer))
while not len(stdout.channel.in_buffer):
    # stdoutにパスワードプロンプトが出力されるまで待ち続ける
    continue
print("buffer size: ", len(stdout.channel.in_buffer))

# sudoパスワード入力
stdin.channel.send("password" + "\n")
# stdinだけ閉じる
stdin.channel.shutdown_write()

# 実行結果
print("-"*20)
print(stdout.read().decode().strip())
# (get_pty=Trueにしていると、stderrもこっちに出力されてしまっている)
print("-"*20)

# 切断
client.close()
