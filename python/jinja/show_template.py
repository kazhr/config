#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("."),
    lstrip_blocks=True
)

template = env.get_template("./template.txt.j2")
rendered = template.render()

print(rendered)
