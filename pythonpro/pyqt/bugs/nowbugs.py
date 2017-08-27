#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os, sys, io
import datetime
from calendar import mdays
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

_MYSQLIP_ = "113.107.161.79"
_MYSQLDB_ = "zentao"
_MYSQLUID_ = "read"
_MYSQLPASS_ = "read"
_MYSQLPORT_ = 3306
path = os.path.dirname(sys.argv[0])

# mysql connect
def GetMysql(sql):
    db = pymysql.connect(host=_MYSQLIP_, port=_MYSQLPORT_, db=_MYSQLDB_, user=_MYSQLUID_, passwd=_MYSQLPASS_, charset="utf8")
    cursor = db.cursor()
    try:
        effect_row = cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    return cursor


# read mysql
def readMysql():
    sql = "SELECT assignedTo FROM zentao.zt_bug WHERE `status` = 'active' AND deleted = '0' ORDER BY assignedTo"
    cursor = GetMysql(sql)
    personCountMap = {}
    data = ""
    for dt in cursor:
        assignedTo = dt[0]
        if assignedTo in personCountMap:
            personCountMap[assignedTo] = personCountMap[assignedTo] + 1
        else:
            personCountMap[assignedTo] = 1

    nNumTotal = cursor.rownumber

    for name in personCountMap:
        sql2 = "SELECT realname FROM zentao.zt_user WHERE account = '" + name + "'"
        cursor2 = GetMysql(sql2)
        realname = ""
        for dt in cursor2:
            realname = dt[0]

        data = data + "{value : " + str(personCountMap[name]) + ", name : \"" + str(realname) + "\"},"

    if data != "":
        data = data[0: len(data) - 1]
    return data, nNumTotal


# 每日新建BUG查询
def get_daily_bug(date, product):
    sql = 'select id from zt_bug where product={product} and openeddate like "{date}%"'.format(product=product, date=date)
    cursor = GetMysql(sql)
    return cursor.rowcount


# 日期比较
def datemin(date, today):
    if int(date[5:7]) > int(today[5:7]):
        return False
    elif int(date[5:7]) == int(today[5:7]):
        if int(date[-2:]) > int(today[-2:]):
            return False
        else:
            return True
    else:
        return True


# 统计每日BUG
def bugs_num(date1, today, isTrue=True):
    allnum = 0
    mydays = mdays
    day_bug = {}
    datetitle = ''
    datenum = ''
    # for i in range(1, 13):
    # if i == 7:
    for j in range(1, mydays[int(date1[5:])]+1):
        if j < 10:
            date = '2017-{0}-0{1}'.format(date1[5:], j)
        else:
            date = '2017-{0}-{1}'.format(date1[5:], j)
        if datemin(date, today):
            if isTrue:
                day_bug[date] = get_daily_bug(date, '1')
                allnum += day_bug[date]
            else:
                day_bug[date] = get_daily_bug(date, '2')
                allnum += day_bug[date]
        else:
            break

    for key, value in day_bug.items():
        datetitle += '\"' + key[5:] + '\"' + ','
        datenum += str(value) + ','

    if datetitle:
        datetitle = datetitle.rstrip(',')

    if datenum:
        datenum = datenum.rstrip(',')

    return datetitle, datenum, allnum


# 写入结果
def write(date, datetitle, datenum, allnum, isTrue=True):
    f = open(os.path.join(path, 'test.html'))
    text = f.readlines()
    f.close()
    text[18] = '				text: \'' + date + '每日BUG数,总计:' + str(allnum) + '\'' + '\n'
    text[45] = '				data: [' + datetitle + ']' + '\n'
    text[61] = '				data: [' + datenum + ']' + '\n'
    if isTrue:
        f = open(os.path.join(path, '国内/' + date + '.html'), 'w')
        f.writelines(text)
        f.close()
    else:
        f = open(os.path.join(path, '海外/' + date + '.html'), 'w')
        f.writelines(text)
        f.close()


#自动新增月份:
def addmonth(date_month):
    date_text = '  <li> <a href="国内/' + date_month + '.html"> ' + date_month + ' </a> </li>\n'
    date_text_over = '  <li> <a href="海外/' + date_month + '.html"> ' + date_month + ' </a> </li>\n'
    print(date_month)
    f = open(os.path.join(path, 'bugs.html'))
    text = f.readlines()
    f.close()
    if text[11] == date_text:
        print('相同')
        pass
    else:
        for i in range(len(text)):
            if '海外/' in text[i]:
                text.insert(11, date_text)
                text.insert(i+1, date_text_over)
                break
        f = open(os.path.join(path, 'bugs.html'), 'w')
        f.writelines(text)
        f.close()


def main(date, today):
    datetitle, datenum , allnum= bugs_num(date, today)
    write(date, datetitle, datenum, allnum)
    datetitle, datenum, allnum= bugs_num(date, today, False)
    write(date, datetitle, datenum, allnum, False)

# for item in ('2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08'):
#     main(item, '2017-08-09')
# # main('2017-08')
date = str(datetime.date.today())
date_month = date[:-3]
addmonth(date_month)
main(date_month, date)
