#!/usr/bin/python3
# -*- coding:utf-8 -*-


import configparser
import os


# 建立configparser 对象

cf = configparser.ConfigParser()

# 创建test.conf
# cf.add_section('更新目录')
# cf.set('更新目录', 'develop_path', 'path')
# cf.set('更新目录', 'test_path', 'path')
#
# cf.add_section('版本号')
# cf.set('版本号', 'new_version', 'HEAD')
# cf.set('版本号', 'old_version', '100')
#
# cf.write(open('/Users/runehero/Desktop/test.conf', 'w'))


# 读取test.conf
cf.read('/Users/runehero/Desktop/test.conf')

develop_path = cf.get('更新目录', 'develop_path')
test_path = cf.get('更新目录', 'test_path')
new_version = cf.get('版本号', 'new_version')
old_version = cf.get('版本号', 'old_version')

print(develop_path, test_path, new_version, old_version)
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
# print(cf.sections())
# print(cf.options('abc'))
# print(cf.items('abc')[1][1])
