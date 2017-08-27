#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import os, sys, io
import time
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

_MYSQLIP_ = "113.107.161.79"
_MYSQLDB_ = "zentao"
_MYSQLUID_ = "read"
_MYSQLPASS_ = "read"
_MYSQLPORT_ = 3306

_CLIENT_NAMES_ = {
            "柏云"       : True, 
            "陈正发"     : True,        
            "邓金良"     : True,        
            "董亮飞"     : True,        
            "胡汉鹏"     : True,        
            "李龙杰"     : True,        
            "石柳"       : True, 
            "徐佼"       : True, 
            "张涛"       : True, 
            "周根清"     : True,        
            "张轩"       : True
            }

#### mysql connect
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

#### read mysql
def readMysql():
    sql = "SELECT assignedTo FROM zentao.zt_bug WHERE `status` = 'active' AND deleted = '0' ORDER BY assignedTo"
    cursor = GetMysql(sql)
    personCountMap = {}
    arrData = []
    
    for dt in cursor:
        assignedTo = dt[0]
        if assignedTo in personCountMap:
            personCountMap[assignedTo] = personCountMap[assignedTo] + 1
        else:
            personCountMap[assignedTo] = 1

    for name in personCountMap:
        arrData.append([name, personCountMap[name]])

    arrData = sorted(arrData, key = lambda da: da[1])
    # arrData.sort(comp)
    
    dataClientTile = ""
    dataClientMsg = ""
    bugClientNum = 0
    
    nNumTotal = cursor.rownumber
    dataTitle = ""
    dataMsg = ""
    # for name in personCountMap:
    for idx in range(len(arrData)):
        info = arrData[len(arrData) - idx - 1]
        name = info[0]
        val = info[1]
        sql2 = "SELECT realname FROM zentao.zt_user WHERE account = '" + name + "' ORDER BY role"
        cursor2 = GetMysql(sql2)
        realname = ""
        for dt in cursor2:
            realname = dt[0]

        dataTitle = dataTitle + "\"" + str(realname) + "\","
        dataMsg = dataMsg + str(val) + ","

        if _CLIENT_NAMES_.get(realname):
            dataClientTile = dataClientTile + "\"" + str(realname) + "\","
            dataClientMsg = dataClientMsg + str(val) + ","
            bugClientNum = bugClientNum + val

        #data = data + "{value : " + str(val) + ", name : \"" + str(realname) + "\"},"
        
    if dataTitle != "":
        dataTitle = dataTitle[0: len(dataTitle) - 1]
    if dataMsg != "":
        dataMsg = dataMsg[0: len(dataMsg) - 1]

    if dataClientTile != "":
        dataClientTile = dataClientTile[0: len(dataClientTile) - 1]
    if dataClientMsg != "":
        dataClientMsg = dataClientMsg[0: len(dataClientMsg) - 1]
    return dataTitle, dataMsg, nNumTotal, dataClientTile, dataClientMsg, bugClientNum


def PrintAll(dataTitle, dataMsg, nNum, dataClientTile, dataClientMsg, bugClientNum):
    print ("Content-type:text/html")
    print ("")
    print ("<!DOCTYPE html>")
    print ("<html>")
    print ("<head>")
    print ("<title>禅道BUG统计</title>")
    print ("    <meta charset=\"utf-8\">")
    print ("    <!-- 引入 ECharts 文件 -->")
    print ("    <script src=\"../echarts.min.js\"></script>")
    print ("</head>")
    print ("<body>")
    print ("<a href=\"index\">返回主页</a>")
    print ("<br />")
    print ("<b style=\"color:red;font-size:30px;\">当前有" + str(nNum) + "个BUG待修复</b>")
    print ("<br/ ><br/ >")
    print ("<!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->")
    print ("    <div id=\"main\" style=\"height:400px;\"></div>")
    print ("    <script type=\"text/javascript\">")
    print ("        // 基于准备好的dom，初始化echarts实例")
    print ("        var myChart = echarts.init(document.getElementById('main'));")
    print ("")
    print ("        // 指定图表的配置项和数据")
    print ("        var option = {")
    print ("                title: {")
    print ("                text: '每日BUG数'")
    print ("            },")
    print ("            tooltip: {},")
    print ("            legend: {")
    print ("                data:['num']")
    print ("            },")
    print ("            xAxis: {")
    print ("                data: [" + dataTitle + "]")
    print ("            },")
    print ("            yAxis: {},")
    print ("            series: [{")
    print ("                name: '',")
    print ("                type: 'bar',")
    print ("                data: [" + dataMsg + "]")
    print ("            }]")
    print ("        };")
    print ("")
    print ("        // 使用刚指定的配置项和数据显示图表。")
    print ("        myChart.setOption(option);")
    print ("    </script>")
    print ("")

    print ("<!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->")
    print ("    <div id=\"main2\" style=\"height:400px;\"></div>")
    print ("    <script type=\"text/javascript\">")
    print ("        // 基于准备好的dom，初始化echarts实例")
    print ("        var myChart = echarts.init(document.getElementById('main2'));")
    print ("")
    print ("        // 指定图表的配置项和数据")
    print ("        var option = {")
    print ("                title: {")
    print ("                text: '客戶端  每日BUG数: " + str(bugClientNum) + "'")
    print ("            },")
    print ("            tooltip: {},")
    print ("            legend: {")
    print ("                data:['num']")
    print ("            },")
    print ("            xAxis: {")
    print ("                data: [" + dataClientTile + "]")
    print ("            },")
    print ("            yAxis: {},")
    print ("            series: [{")
    print ("                name: '',")
    print ("                type: 'bar',")
    print ("                data: [" + dataClientMsg + "]")
    print ("            }]")
    print ("        };")
    print ("")
    print ("        // 使用刚指定的配置项和数据显示图表。")
    print ("        myChart.setOption(option);")
    print ("    </script>")
    print ("")
    print ("<a href=\"javascript:location.reload();\">点击刷新页面</a>")
    print ("<br /><br />")
    print ("<a href=\"#\" onClick=\"javascript :history.back(-1);\">返回上一页</a>")
    print ("<br /><br />")
    print ("</body>")
    print ("</html>")
    return

def main():
    dataTitle, dataMsg, nNum, dataClientTile, dataClientMsg, bugClientNum = readMysql()
    PrintAll(dataTitle, dataMsg, nNum, dataClientTile, dataClientMsg, bugClientNum)
    return

main()

