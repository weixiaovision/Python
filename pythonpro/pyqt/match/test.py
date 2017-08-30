#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import re
import sys
import codecs


def match(string1):
    for root, dirs, files in os.walk('.'):
        for file in files:
            text = codecs.open(os.path.join(root, file), 'r', 'utf-8')
            lines = text.readlines()
            text.close()
            for i in range(len(lines)):
                if re.search(string1, lines[i]):
                    print(os.path.join(root, file), '第', i+1, '行：', string1)


def readconfig():
    stringlist = []
    text = codecs.open('match.xml', 'r', 'utf-8')
    lines = text.readlines()
    text.close()
    for line in lines:
        stringlist.append(line.strip())
    return stringlist

def main():
    stringlist = readconfig()
    for string1 in stringlist:
        match(string1)

if __name__ == '__main__':
    main()