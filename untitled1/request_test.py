#!/usr/bin/python3
# -*- coding:utf-8 -*-


import requests
from bs4 import BeautifulSoup


response = requests.get('http://aosabook.org/en/500L/web-server/testpage.html')
print(response.status_code)
print(response.text)
print(response.headers['content-length'])
print(response.cookies)
r = BeautifulSoup(response.text, "html.parser")
print(r.p.text)
print(r.title)
print(r.body.text)
