#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import docker
import time


class DockerSDK:

    client = docker.from_env()
    delay = 10  # [s]
    name = None

    def get(self):
        """
        コンテナ取得
        """
        try:
            container = self.client.containers.get(self.name)
        except docker.errors.NotFound:
            emsg = "Please up the container first."
            raise docker.errors.NotFound(emsg)
        return container

    def start(self):
        """
        コンテナ起動
        """
        container = self.get()
        if container.status == "exited":
            container.start()
            # wait for starting
            time.sleep(self.delay)

    def stop(self):
        """
        コンテナ停止
        """
        container = self.get()
        if container.status == "running":
            container.stop()

    def down(self):
        """
        コンテナ削除
        """
        self.stop()
        container = self._get()
        container.remove()


class DockerMySQL(DockerSDK):
    """
    mysqlコンテナ操作
    """
    def __init__(self, name="mysql", image="mysql:5.7"):
        self.name = name
        self.image = image

    def up(self):
        """
        コンテナ作成
        """
        self.client.containers.run(
            name=self.name,
            image=self.image,
            ports={
                "3306/tcp": ("127.0.0.1", 3306),
            },
            environment={
                "MYSQL_ROOT_PASSWORD": "root_password",
                "MYSQL_DATABASE": "database",
                "MYSQL_USER": "user",
                "MYSQL_PASSWORD": "password",
                "TZ": "Asia/Tokyo",
            },
            command="mysqld --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci",
            detach=True,
        )
        # wait for starting
        time.sleep(self.delay)
