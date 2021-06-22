#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument(
    "--input",
    default="./ansible.log",
    help="Ansible実行ログのファイルパス"
)


def load(log_file):

    if not log_file.exists():
        emsg = f"not found {log_file}!"
        raise ValueError(emsg)

    # load
    with log_file.open("r") as obj:
        lines = obj.readlines()

    # compile
    re_task = re.compile(r"(?<=\[).*(?=\])")

    # store
    data = {}

    for line in lines:

        line = line.strip()

        if line.startswith("TASK"):
            task = re_task.search(line).group(0)
            data[task] = {}
            data[task]["is_handler"] = False
            data[task]["changed"] = False

        elif line.startswith("RUNNING HANDLER"):
            task = re_task.search(line).group(0)
            data[task] = {}
            data[task]["is_handler"] = True
            data[task]["changed"] = False

        elif line.startswith("--- before:"):
            data[task]["changed_item"] = line[12:]

        elif line.startswith("-"):
            if "before" not in data[task]:
                data[task]["before"] = []
            data[task]["before"].append(line)

        elif line.startswith("+"):
            if "after" not in data[task]:
                data[task]["after"] = []
            data[task]["after"].append(line)

        elif line.startswith("changed"):
            data[task]["changed"] = True

    return data


if __name__ == "__main__":

    args = parser.parse_args()
    log_file = Path(args.input)

    data = load(log_file)

    for task_name, task_info in data.items():
        if task_info["is_handler"]:
            continue

        if not task_info["changed"]:
            continue

        if "before" not in task_info and "after" not in task_info:
            print(task_name)
