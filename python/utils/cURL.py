#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json


class cURL:
    def post_json(self, url, data):
        return requests.post(
            url,
            json.dumps(data),
            headers={'Content-Type': 'application/json'},
        )
