#!/usr/bin/python3
# -*- coding:utf-8 -*-


import configparser
import os


# 建立configparser 对象

cf = configparser.ConfigParser()

# # 创建test.conf
# cf.add_section('abc')
# cf.set('abc', 'version', '1.0.0')
# cf.set('abc', 'name', 'vision')

# cf.write(open('/Users/runehero/Desktop/test.conf', 'w'))

# 读取test.conf
cf.read('/Users/runehero/Desktop/test.conf')

# 修改配置
# cf.add_section('test')
# cf.set('test', 'price', '200')
# cf.write(open('/Users/runehero/Desktop/test.conf', 'w'))

# 获取数据

# price = cf.getint('test', 'price')
#
# print(price)
# print(type(price))

# print(cf.getint('abc', 'version'))
print(cf.sections())
print(cf.options('abc'))
print(cf.items('abc')[1][1])
