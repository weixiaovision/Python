#!/usr/bin/python3
# -*- coding:utf-8


import xml.etree.ElementTree as et
import os
import sys


path = os.path.dirname(sys.argv[0])
tree = et.parse(os.path.join(path, 'module.xml'))
root = tree.getroot()
combat_list = []
social_list = []
activity_list = []
servererror__list = []
other_list = []
for item in root[0]:
    combat_list.append(item.attrib['id'])

for item in root[1]:
    social_list.append(item.attrib['id'])

for item in root[2]:
    activity_list.append(item.attrib['id'])

for item in root[3]:
    servererror__list.append(item.attrib['id'])

for item in root[4]:
    other_list.append(item.attrib['id'])


