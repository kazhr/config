#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import sys

env = Environment(
    loader=FileSystemLoader("."),
    lstrip_blocks=True
)

template = env.get_template(sys.argv[1])
rendered = template.render()

print(rendered)
