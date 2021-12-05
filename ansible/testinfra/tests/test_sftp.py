#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import tempfile


class TestSFTP:
    """
    外部からsftpのテスト
    """
    # sftp専用のユーザー
    username = "sftp_user"
    password = "password"
    ssh_port = 10022
    root_dir = "data"

    def get_target(self, host):
        """
        asnible_hostから読み込む場合処理を追加
        (ansible_backendsを使用しているときのみ有効)
        """
        return "localhost"

    def test_ssh_disabled(self, host):
        """
        sftp専用のユーザーはsshができないこと
        """
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.get_target(host),
                username=self.username,
                password=self.password,
                port=self.ssh_port,
            )
            stdin, stdout, stderr = ssh_client.exec_command(
                "whoami",
                timeout=3,
                get_pty=False
            )
            stdout = stdout.read().decode().strip()
        assert stdout == "This service allows sftp connections only."

    def test_sftp_dir_operation(self, host):
        """
        sftp接続でフォルダ操作ができること
        """
        # テストフォルダ名
        test_dname = "test_dir"

        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.get_target(host),
                username=self.username,
                password=self.password,
                port=self.ssh_port,
            )
            sftp_connection = ssh_client.open_sftp()
            sftp_connection.chdir(self.root_dir)

            # 前提としてテスト用のフォルダが存在しないこと
            entries = sftp_connection.listdir()
            assert test_dname not in entries

            # テスト用のフォルダが作成できること
            sftp_connection.mkdir(test_dname)
            entries = sftp_connection.listdir()
            assert test_dname in entries

            # テスト用のフォルダが削除できること
            sftp_connection.rmdir(test_dname)
            entries = sftp_connection.listdir()
            assert test_dname not in entries

    def test_sftp_file_operation(self, host):
        """
        sftp接続でファイル操作ができること
        """
        # テストファイル名
        test_fname = "test.txt"
        test_text = "This is a test file."

        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.get_target(host),
                username=self.username,
                password=self.password,
                port=self.ssh_port,
            )
            sftp_connection = ssh_client.open_sftp()
            sftp_connection.chdir(self.root_dir)

            # 前提としてテストファイルが存在しないこと
            entries = sftp_connection.listdir()
            assert test_fname not in entries

            # テストファイルがPUTできること
            with tempfile.NamedTemporaryFile(mode="w") as fp:
                fp.write(test_text)
                # ポインタを先頭に戻す
                fp.seek(0)
                sftp_connection.put(fp.name, test_fname)
            entries = sftp_connection.listdir()
            assert test_fname in entries

            # テストファイルがGETできること
            with tempfile.NamedTemporaryFile(mode="r") as fp:
                sftp_connection.get(test_fname, fp.name)
                received_message = fp.read()
            # 受信したファイルの中身が一致すること
            assert received_message == test_text

            # テストファイルが削除できること
            sftp_connection.remove(test_fname)
            entries = sftp_connection.listdir()
            assert test_fname not in entries
