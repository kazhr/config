#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
import socket

app = FastAPI()


@app.get("/api/{ip}/name")
async def get_hostname(ip: str):
    """
    IP -> FQDN
    """
    return {"result": socket.getfqdn(ip)}


@app.get("/api/{hostname}/ip")
async def get_ip(hostname: str):
    """
    FQDN -> IP
    """
    return {"result": socket.gethostbyname(hostname)}
