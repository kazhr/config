#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import contextmanager
import paramiko
import textwrap


class Telnet(object):
    """
    Generate bash scripts for automating telnet session.

    Parameters
    ----------
    hostname : str

    username : str

    password : str

    port : int, default=23

    sleep : int, default=1
        Interval in seconds for waiting the telnet serverresponse.
        Please increae if the response is slow.
    """

    def __init__(self, hostname, username, password,
                 port=23, sleep=1):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.sleep = sleep

    def _wrap(self, cmds):

        self.login_message = "Login successed!"
        self.logout_message = "Finished, bye."

        wrapped = textwrap.dedent(f"""
        ( sleep {self.sleep}; echo {self.username}; \\
          sleep {self.sleep}; echo {self.password}; \\
          sleep {self.sleep}; echo 'echo {self.login_message}'; \\
          {cmds}\\
          sleep {self.sleep}; echo 'echo {self.logout_message}'; \\
          sleep {self.sleep}; echo quit \\
        )| telnet {self.hostname} {self.port}
        """).strip()
        self.total_sleep += self.sleep*5

        print(f"This task will take {self.total_sleep}s.")
        return wrapped

    def get_oneliner(self, cmds, sleep=None):
        """
        Return a one-line command to execute input commands on the remote.

        Parameters
        ----------
        cmds : list of str

        sleep : int, default=None
            If None, self.sleep will be used.
            Please increae when running commands that takes time to execute.
        """

        if not isinstance(cmds, list):
            cmds = [cmds]
        if sleep is None:
            sleep = self.sleep

        oneliner = ""
        total_sleep = 0
        for cmd in cmds:
            oneliner += f"sleep {sleep}; echo '{cmd}'; "
            total_sleep += sleep

        self.cmds = cmds
        self.total_sleep = total_sleep

        return self._wrap(oneliner)

    def get_results(self, stdout):
        """
        Get command results from the stdout.

        Returns
        -------
        dict
        """

        # remove carriage Return
        stdout = stdout.replace("\r", "")
        # remove "ESC Code Sequence: request cursor position"
        stdout = stdout.replace("\x1b[6n", "")

        lines = stdout.split("\n")
        # read line index
        for i, line in enumerate(lines):
            if line == self.login_message:
                start_index = i + 1
                break
        else:
            emsg = f"can not find {self.login_message}"
            raise ValueError(emsg)

        index = []
        for cmd in self.cmds:
            for i, line in enumerate(lines[start_index:]):
                if line.endswith(cmd):
                    start_index += i
                    index.append(start_index)
                    break
            else:
                emsg = f"can not find {cmd} in the stdout"
                raise ValueError(emsg)

        for i, line in enumerate(lines[start_index:]):
            if line == self.logout_message:
                end_index = start_index + i - 1
                index.append(end_index)
                break
        else:
            emsg = f"can not find {self.logout_message}"
            raise ValueError(emsg)

        # read the cmd results
        results = {}
        for i, cmd in enumerate(self.cmds):
            results[cmd] = "\n".join(lines[index[i]+1:index[i+1]])

        return results


class SSHClient(object):
    """
    SSH agent using paramiko

    Parameters
    ----------
    hostname : str

    username : str

    password : str, optional
        if None, pkeyfile is required. default=None

    pkeyfile: str|Path, optional
        ssh private key file path

    port : int, optional
        default=22

    policy : "AutoAdd"|"Warging"|"Reject", optional
        default="AutoAdd"

    timeout : int, optional
        default=5
    """

    def __init__(self, hostname, username,
                 password=None, pkeyfile=None,
                 port=22, policy="AutoAdd", timeout=5):

        policy = {
            "AutoAdd": paramiko.AutoAddPolicy(),
            "Warning": paramiko.WarningPolicy(),
            "Reject": paramiko.RejectPolicy(),
        }[policy]

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(policy)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.pkeyfile = pkeyfile
        self.port = port
        self.timeout = timeout

    @contextmanager
    def connect(self):
        """
        Connect to the host.
        """
        self.client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            key_filename=self.pkeyfile,
            timeout=self.timeout,
        )
        try:
            yield self.client
        finally:
            self.client.close()

    def run(self, command):
        """
        Execute a command on the remote.

        Parameters
        ----------
        commands : str

        Returns
        -------
        stdout : str
        stderr : str
        """
        with self.connect() as client:
            _, stdout, stderr = client.exec_command(command)
            stdout = stdout.read().decode().strip()
            stderr = stderr.read().decode().strip()
        return stdout, stderr


if __name__ == "__main__":

    telnet = Telnet(
        hostname="telnetd",
        username="telnet",
        password="password",
        sleep=0.1,
    )
    cmd = telnet.get_oneliner(["whoami", "id"])

    ssh = SSHClient(
        hostname="localhost",
        username="developer",
        pkeyfile="./ssh_nopass/id_ed25519",
    )
    stdout, stderr = ssh.run(cmd)

    for key, value in telnet.get_results(stdout).items():
        print(key, ":", value)
