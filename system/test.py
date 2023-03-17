#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-11 18:35
# @Author  : myloe
# @File    : test.py

import requests

def send_request(name):
    res = requests.request('get', f"http://0.0.0.0:8000/system/test?name={name}")
    print(f"{name} --> res")
    return "ok"

for i in range(20):
    try:
        name = "a"
        requests.get("http://127.0.0.1:8000/test/",timeout=0.1)
        requests.request('get', f"http://0.0.0.0:8000/system/test?name={name}", timeout=0.01)
    except requests.exceptions.ReadTimeout:
        pass

for i in range(20):
    try:
        name = 'b'
        requests.get("http://127.0.0.1:8000/test/",timeout=0.1)
        requests.request('get', f"http://0.0.0.0:8000/system/test?name={name}", timeout=0.01)
    except requests.exceptions.ReadTimeout:
        pass

for i in range(20):
    try:
        name="c"
        requests.get("http://127.0.0.1:8000/test/",timeout=0.1)
        requests.request('get', f"http://0.0.0.0:8000/system/test?name={name}", timeout=0.01)
    except requests.exceptions.ReadTimeout:
        pass