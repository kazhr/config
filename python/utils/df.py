#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

stat = os.statvfs("/")


Blocks1K = stat.f_blocks
Available = stat.f_bfree
Used = Blocks1K - Available

Use = Used / Blocks1K * 100
print(f"disk_usage = {Use} %")


Inodes = stat.f_files
IFree = stat.f_ffree
IUsed = Inodes - IFree

IUse = IUsed / Inodes * 100
print(f"inode_usage = {IUse} %")
