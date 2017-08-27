#!/usr/bin/python3
# -*- coding:utf-8 -*-


import xml.etree.ElementTree as et
import sys
import os
import pymysql


_MYSQLIP_ = "113.107.161.79"
_MYSQLDB_ = "zentao"
_MYSQLUID_ = "read"
_MYSQLPASS_ = "read"
_MYSQLPORT_ = 3306
combat_list = []
social_list = []
activity_list = []
servererror_list = []
other_list = []
path = os.path.dirname(sys.argv[0])
module_count = {}


# mysql connect
def GetMysql(sql):
    db = None
    cursor = None
    result = None
    try:
        db = pymysql.connect(host=_MYSQLIP_, port=_MYSQLPORT_, db=_MYSQLDB_, user=_MYSQLUID_, passwd=_MYSQLPASS_,
                             charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
    if db:
        db.close()
    if cursor:
        cursor.close()
    if result:
        return result
    return result


# get config
def init_config():
    path = os.path.dirname(sys.argv[0])
    tree = et.parse(os.path.join(path, 'module.xml'))
    root = tree.getroot()

    for item in root[0]:
        combat_list.append(item.attrib['id'])

    for item in root[1]:
        social_list.append(item.attrib['id'])

    for item in root[2]:
        activity_list.append(item.attrib['id'])

    for item in root[3]:
        servererror_list.append(item.attrib['id'])

    for item in root[4]:
        other_list.append(item.attrib['id'])
    return combat_list, social_list, activity_list, servererror_list, other_list

# 查询统计

def main(openedbuild):
    result_module = ''
    init_config()
    combat_count = 0
    social_count = 0
    activity_count = 0
    serevererror_count = 0
    other_count = 0
    add_count = 0
    sql = 'SELECT module,COUNT(module) FROM zt_bug WHERE product=1 AND openedBuild={0} GROUP BY module'.format(openedbuild)
    result = GetMysql(sql)
    if result:
        for item in result:
            if str(item[0]) in combat_list:
                combat_count += item[1]
            elif str(item[0]) in social_list:
                social_count += item[1]
            elif str(item[0]) in activity_list:
                activity_count += item[1]
            elif str(item[0]) in servererror_list:
                serevererror_count += item[1]
            elif str(item[0]) in other_list:
                other_count += item[1]
            else:
                add_count += item[1]
    module_count['战斗系统'] = combat_count
    module_count['社交系统'] = social_count
    module_count['活动相关'] = activity_count
    module_count['服务器、bugly报错'] = serevererror_count
    module_count['其他'] = other_count
    module_count['新增模块'] = add_count
    for key, value in module_count.items():
        result_module += '{' + 'value : ' + str(value) + ',' + 'name' + ' : ' + '\"' + key + '\"' + '}' + ','
    result_module = result_module.rstrip(',')
    print(result_module)

main('13')
