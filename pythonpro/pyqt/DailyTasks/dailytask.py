#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QCheckBox, QLineEdit, QComboBox
import view
import xml.etree.ElementTree as ET
import time
import requests
import json
from threading import Thread
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import queue
import os

class MyThread(Thread):

    def __init__(self, name, sched):
        Thread.__init__(self)
        self.name = name
        self.sched = sched

    def run(self):
        print('开启线程')
        if self.sched:
            self.sched.start()

    def stop(self):
        print('关闭调度qi')
        if self.sched:
            self.sched.shutdown(wait=False)


class MainWindow(QMainWindow, view.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.rowcount = 0
        self.checklist = []
        self.today = time.strftime('%Y-%m-%d')
        self.task = self.readconfig()
        self.thread = None

    def run(self):
        self.view.nameLineEdit.setText(self.task[0])
        self.insert_task()
        self.sendtimingtask()
        self.view.addPushButton.clicked.connect(self.add_tasktablewidget)
        self.view.pushButton.clicked.connect(lambda: self.sendmessage(False))
        self.view.comboBox.currentTextChanged.connect(self.time_reset)
        self.view.show()
        sys.exit(self.app.exec_())

    def readconfig(self):
        task_list = []
        tree = ET.parse('task.xml')
        root = tree.getroot()
        for child in root:
            task_list.append(child.text)
        return task_list

    def insert_task(self):
        if os.path.exists('ini'):
            f = open('ini', encoding='utf-8')
            text = f.readlines()
            f.close()
            if text[0].strip() == self.today:
                self.insert_tasetable_today(text)
            else:
                self.insert_tasktablewidget()
        else:
            self.insert_tasktablewidget()

    def insert_tasktablewidget(self):
        self.view.taskTableWidget.setRowCount(len(self.task)-1)
        for i in range(len(self.task)-1):
            daytime = QTableWidgetItem(self.today)
            self.view.taskTableWidget.setItem(i, 0, daytime)
            checkbutton = QCheckBox()
            self.view.taskTableWidget.setCellWidget(i, 1, checkbutton)
            lineEdit2 = QLineEdit()
            lineEdit2.setText(self.task[i+1])
            self.view.taskTableWidget.setCellWidget(i, 2, lineEdit2)
            progress = QComboBox()
            progress.setEditable(True)
            progress.addItems(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
            self.view.taskTableWidget.setCellWidget(i, 3, progress)
            progress.currentIndexChanged.connect(self.writetask)
            lineEdit = QLineEdit()
            self.view.taskTableWidget.setCellWidget(i, 4, lineEdit)
            self.checklist.append([checkbutton, lineEdit2, progress, lineEdit])
        self.rowcount = len(self.task) - 1

    def insert_tasetable_today(self, text):
        self.view.taskTableWidget.setRowCount(len(text)-1)
        for i in range(len(text)-1):
            item = text[i+1].split(':')
            daytime = QTableWidgetItem(self.today)
            self.view.taskTableWidget.setItem(i, 0, daytime)
            checkbutton = QCheckBox()
            self.view.taskTableWidget.setCellWidget(i, 1, checkbutton)
            lineEdit2 = QLineEdit()
            lineEdit2.setText(item[0])
            self.view.taskTableWidget.setCellWidget(i, 2, lineEdit2)
            progress = QComboBox()
            progress.addItems(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
            progress.setEditable(True)
            progress.setCurrentIndex(int(item[2]))
            self.view.taskTableWidget.setCellWidget(i, 3, progress)
            progress.currentIndexChanged.connect(self.writetask)
            lineEdit = QLineEdit()
            lineEdit.setText(item[3])
            self.view.taskTableWidget.setCellWidget(i, 4, lineEdit)
            self.checklist.append([checkbutton, lineEdit2, progress, lineEdit])
        self.rowcount = len(text)


    def add_tasktablewidget(self):
        self.view.taskTableWidget.setRowCount(self.rowcount + 1)
        daytime = QTableWidgetItem(self.today)
        self.view.taskTableWidget.setItem(self.rowcount, 0, daytime)
        checkbutton = QCheckBox()
        self.view.taskTableWidget.setCellWidget(self.rowcount, 1, checkbutton)
        lineEdit2 = QLineEdit()
        self.view.taskTableWidget.setCellWidget(self.rowcount, 2, lineEdit2)
        progress = QComboBox()
        progress.addItems(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
        progress.setEditable(True)
        self.view.taskTableWidget.setCellWidget(self.rowcount, 3, progress)
        progress.currentIndexChanged.connect(self.writetask)
        lineEdit = QLineEdit()
        self.view.taskTableWidget.setCellWidget(self.rowcount, 4, lineEdit)
        self.checklist.append([checkbutton, lineEdit2, progress, lineEdit])
        self.rowcount += 1

    # 发送任务进度给指定人
    def sendmessage(self, sendme=True):
        print('执行发送任务')
        taskall = ''
        if self.view.checkBox.checkState():
            print(111111111)
            for item in self.checklist:
                # if item[0].checkState() and item[2].currentText() != '100%':
                if item[2].currentText() != '100%':
                    strInfo = item[1].text() + '     ' + item[2].currentText()
                    taskall += strInfo + '\n'
                    if item[0].checkState():
                        if item[3].text():
                            self.sendRTX(strInfo, item[3].text().split(','))
            if sendme:
                if taskall and self.view.nameLineEdit.text():
                    self.sendRTX(taskall, [self.view.nameLineEdit.text()])

    # rtx发送消息方法
    def sendRTX(self, strInfo, usernamelist):
        params = {
            "msg_title": "今日任务提醒",
            "msg_content": strInfo,
            "receiver": [{}]
        }
        for username in usernamelist:
            print(username)
            temp = {"user_name": username, "domain": ""}
            params['receiver'].append(temp)
        # for each in _MYSQLBUGMAP_:
        #     temp = {"user_name": _MYSQLBUGMAP_[each].userRtxName, "domain": ""}
        #     params["receiver"].append(temp)

        # temp = {"user_name": "ang", "domain": ""}
        # params["receiver"].append(temp)
        # temp = {"user_name": "tim.ng", "domain": ""}
        # params["receiver"].append(temp)
        # temp = {"user_name": "zeyuan.chen", "domain": ""}
        # params["receiver"].append(temp)
        # temp = {"user_name": "smith", "domain": ""}
        # params["receiver"].append(temp)

        data = json.JSONEncoder().encode(params)
        result = None
        try:
            response = requests.post("http://10.10.7.103/tips/simple", data.encode(encoding='UTF8'))
            result = response.text
        except Exception as e:
            self.showdialog('发送失败', str(e))
        if result:
            if result[8:11] == '200':
                pass
            else:
                self.showdialog('推送给%s任务未成功发送' % username)

    # 开启推送线程
    def run_threading(self):
        self.thread = MyThread('my_thread', self.sendtimingtask())
        self.thread.setDaemon(True)
        self.thread.start()

    def test(self):
        print(threading.active_count())
        print(threading.enumerate())
        print('test')

    # 设置时间修改时 重启线程
    def time_reset(self):
        if self.thread:
            if self.thread.isAlive:
                print('关闭定时任务')
                self.thread.stop()
        self.run_threading()

    # 固定时间间隔推送
    def sendtimingtask(self):
        print('定时任务开启')
        sched = BlockingScheduler()
        if self.view.comboBox.currentText():
            trigger = IntervalTrigger(minutes=int(self.view.comboBox.currentText()))
            sched.add_job(self.sendmessage, trigger, id='my_job')
            return sched

    # 5分钟写入一次日志
    def timingtask(self, minutes=30):
        sched = BlockingScheduler()
        trigger = IntervalTrigger(minutes=minutes)
        sched.add_job(self.writetask, trigger, id='my_job')
        sched.start()
        return sched

    def timingtask_reset(self):
        self.sched.remove_job('my_job')
        self.sched = self.timingtask(int(40))

    # 写日志
    def writetask(self):
        print('开始写日志')
        if not os.path.isdir('log'):
            os.makedirs('log')
        # time.sleep(0.1)
        f = open('log/%s.log' % self.today, 'a+', encoding='utf-8')
        f.write(time.strftime('%H:%M:%S') + '\n')
        for message in self.checklist:
            f.write('    ' + message[1].text() + '   ' + message[2].currentText() + '   ' + message[3].text() + '\n')
        f.write('\n')
        f.close()
        # 开启写缓存
        dailytext = open('ini', 'w', encoding='utf-8')
        dailytext.write(self.today + '\n')
        for message in self.checklist:
            index = str(message[2].currentIndex())
            dailytext.write(message[1].text() + ':' + message[2].currentText() + ':' +
                            index + ':' + message[3].text() + ':' + '\n')
        dailytext.close()

    # 获取昨日未完成任务给自己
    def get_task(self, path):
        f = open(path, encoding='utf-8')
        text = f.readlines()
        f.close()
        strinfo = None
        for item in text:
            itemsp = item.split(':')
            if itemsp[1] != '100%':
                strinfo += itemsp[0] + '   ' + itemsp[1] + '   ' + itemsp[3] + '\n'
        return strinfo

    def showdialog(self, message, detailmessage=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        if detailmessage:
            msg.setDetailedText(detailmessage)
        msg.setWindowTitle("提示信息")
        msg.exec_()

if __name__ == '__main__':
    client = Client()
    client.run()
