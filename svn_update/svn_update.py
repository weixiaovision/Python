#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os
import sys
import zipfile


zipfile = zipfile.ZipFile('iTerm2-3_0_15.zip')
for file in zipfile.namelist():
    print(file)
