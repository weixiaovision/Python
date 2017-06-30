#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os
import sys


path = os.getcwd()
# print(os.path.realpath(sys.argv))
filename = os.path.realpath(sys.argv[0])
f = open('filename.txt', 'w')
for root, dirs, files in os.walk(path):
    for file in files:
        if file not in (os.path.basename(filename), 'filename.txt'):
            print(file)
            f.writelines(file + '\n')

