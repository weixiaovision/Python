#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import codecs
import pymysql.cursors
import configparser
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication, QMessageBox,   QTableWidgetItem
import view


class MainWindow(QDialog, view.Ui_skillselect):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.insert_combobox(self.read_config_sections('server.conf'))
        self.view.skillLineEdit.returnPressed.connect(self.insert_skillid)
        self.view.skillListWidget.itemClicked.connect(self.item_click)
        self.view.buffLineEdit.returnPressed.connect(self.insert_buff_new)
        self.view.buffListWidget.itemClicked.connect(self.item_click_new)

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

    # 连接数据库
    def connect_db(self):
        self.read_config_sections('server.conf', self.view.comboBox.currentText())
        try:
            self.coon = pymysql.connect(host=self.host,
                                        user=self.user,
                                        port=self.port,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8'
                                        )
        except Exception as e:
            self.showdialog('数据库连接失败', str(e))
            sys.exit()

    # 查询数据库
    def select(self, args=None):
        cursor = None
        result = None
        try:
            self.connect_db()
            cursor = self.coon.cursor()
            cursor.execute(args)
            result = cursor.fetchall()
            return result
        except Exception as e:
            self.showdialog('数据查询失败', str(e))
            sys.exit()
        finally:
            if cursor:
                cursor.close()
            self.coon.close()

    # 插入技能列表，技能模糊搜索
    def insert_skillid(self):
        self.view.skillListWidget.clear()
        self.clear()
        namelike = self.view.skillLineEdit.text()
        if namelike:
            result = self.select('select SkillID,Name from t_s_skill WHERE NAME like "%{abc}%"'.format(abc=namelike))
            if len(result) > 0:
                for item in result:
                    self.view.skillListWidget.addItem(str(item[0]) + '  ' + item[1])
            else:
                self.view.skillListWidget.addItem('查询结果为空')

    # 插入buff列表，buff模糊搜索
    def insert_buff_new(self):
        self.view.buffListWidget.clear()
        self.clear_new()
        namelike = self.view.buffLineEdit.text()
        if namelike:
            result = self.select('select ID,Name from t_s_buffer WHERE NAME like "%{abc}%"'.format(abc=namelike))
            if len(result) > 0:
                for item in result:
                    self.view.buffListWidget.addItem(str(item[0]) + '  ' + item[1])
            else:
                self.view.buffListWidget.addItem('查询结果为空')

    # 开始查询主入口-技能-->buff-->bomb
    def item_click(self):
        self.clear()
        id = None
        # 获取模糊搜索结果中选中的条目
        id_name = self.view.skillListWidget.currentItem().text()
        if id_name:
            if len(id_name.split()) > 1:
                id =id_name.split()[0]
        if id:
            self.insert_skillall(id)
            bufflist = self.insert_buff(id)
            if len(bufflist) > 0:
                self.insert_buffall(bufflist)
                bomblist = self.insert_bomb(bufflist)
                if len(bomblist) > 0:
                    self.insert_bomball(bomblist)

    # 开始查询主入口-buff-->bomb and buff-->skill
    def item_click_new(self):
        self.clear_new()
        buffid = None
        bufflist = []
        # 获取模糊搜索结果中选中的条目
        buff_name = self.view.buffListWidget.currentItem().text()
        if buff_name:
            if len(buff_name.split()) > 1:
                buffid = buff_name.split()[0]
        if buffid:
            self.insert_buffall_new(buffid)
            bufflist.append(buffid)
            self.insert_buffall(bufflist)
            bomblist = self.insert_bomb(bufflist)
            if len(bomblist) > 0:
                self.insert_bomball(bomblist)
            self.insert_skill_new(buffid)

    # 清空历史记录
    def clear(self):
        self.view.buffListWidget.clear()
        self.view.bombListWidget.clear()
        self.view.skillTableWidget.clearContents()
        self.view.buffTableWidget.clearContents()
        self.view.bombTableWidget.clearContents()

    def clear_new(self):
        self.view.skillListWidget.clear()
        self.view.bombListWidget.clear()
        self.view.skillTableWidget.clearContents()
        self.view.buffTableWidget.clearContents()
        self.view.bombTableWidget.clearContents()

    # 技能插入list和表格
    def insert_skill_new(self, buffid):
        skill_name_list = []
        sql = "SELECT a.* FROM t_s_skill a,t_s_buffer b WHERE a.Buff LIKE CONCAT('%%',%s,'%%') GROUP BY a.SkillID" % buffid
        skill_all = self.select(sql)
        self.view.skillTableWidget.setRowCount(len(skill_all))
        i = 0
        for skill in skill_all:
            skill_name_list.append(str(skill[0]) + '   ' + str(skill[1]))
            for j in range(len(skill)):
                item = skill[j]
                item = QTableWidgetItem(str(item))
                self.view.skillTableWidget.setItem(i, j, item)
            i += 1
        if len(skill_name_list) > 0:
            for item in skill_name_list:
                self.view.skillListWidget.addItem(item)
        else:
            self.view.skillListWidget.addItem('此技能没有配置buff')

    # 技能查询结果插入表格
    def insert_skillall(self, id):
        self.view.skillTableWidget.setRowCount(1)
        skill_all = self.select('select * from t_s_skill where skillid = %s' % id)
        if skill_all:
            for i in range(len(skill_all[0])):
                item = QTableWidgetItem(str(skill_all[0][i]))
                self.view.skillTableWidget.setItem(0, i, item)

    # buff查询结果插入表格
    def insert_buffall_new(self, buffid):
        self.view.buffTableWidget.setRowCount(1)
        buff_all = self.select('select * from t_s_buffer where id = %s' % buffid)
        if buff_all:
            for i in range(len(buff_all[0])):
                item = QTableWidgetItem(str(buff_all[0][i]))
                self.view.buffTableWidget.setItem(0, i, item)

    # buff查询结果加入到buff列表
    def insert_buff(self, id):
        buff = self.select('select buff from t_s_skill where skillid=%s' % id)
        bufflist = buff[0][0].split('|')
        buff_name_list = []
        for item in bufflist:
            buff_name = self.select('select ID,Name from t_s_buffer where id=%s' % item)
            if len(buff_name) > 0:
                buff_name_list.append(str(buff_name[0][0]) + '   ' + buff_name[0][1])
        if len(buff_name_list) > 0:
            for item1 in buff_name_list:
                self.view.buffListWidget.addItem(item1)
        else:
            self.view.buffListWidget.addItem('此技能没有配置buff')
            bufflist = []
        return bufflist

    # buff查询结果插入表格
    def insert_buffall(self, bufflist):
        self.view.buffTableWidget.setRowCount(len(bufflist))
        i = 0
        for buff in bufflist:
            buff_all = self.select('select * from t_s_buffer where id = %s' % buff)
            for j in range(len(buff_all[0])):
                item = buff_all[0][j]
                item = QTableWidgetItem(str(item))
                self.view.buffTableWidget.setItem(i, j, item)
            i += 1

    # 读取数据库配置文件
    def read_config_sections(self, config_path, section=None):
        cf = configparser.ConfigParser()
        cf.read_file(codecs.open(config_path, 'r', 'utf-8'))
        if not section:
            return cf.sections()
        else:
            values = cf.items(section)
            self.host = values[0][1]
            self.port = int(values[1][1])
            self.user = values[2][1]
            self.password = values[3][1]
            self.db = values[4][1]

    # 插入数据库comboBox
    def insert_combobox(self, dblist):
        self.view.comboBox.addItems(dblist)

    def insert_bomb(self, bufflist):
        bomblist = []
        bomb_name_list = []
        for buff in bufflist:
            effect = self.select('select effect from t_s_buffer where ID=%s' % buff)[0][0]
            if effect.startswith('Bomb'):
                bomb = effect.split('(')[1]
                bomblist.append(bomb.split(',')[0])
        if len(bomblist) > 0:
            for item in bomblist:
                bomb_name = self.select('select ID,Name from t_s_bomb where id=%s' % item)
                bomb_name_list.append(str(bomb_name[0][0]) + '   ' + bomb_name[0][1])
            if len(bomb_name_list) > 0:
                for item1 in bomb_name_list:
                    self.view.bombListWidget.addItem(item1)
        return bomblist

    # bomb查询结果插入表格
    def insert_bomball(self, bomblist):
        self.view.bombTableWidget.setRowCount(len(bomblist))
        i = 0
        for bomb in bomblist:
            bomb_all = self.select('select * from t_s_bomb where id = %s' % bomb)
            for j in range(len(bomb_all[0])):
                item = bomb_all[0][j]
                item = QTableWidgetItem(str(item))
                self.view.bombTableWidget.setItem(i, j, item)
            i += 1

    # 弹框提示
    def showdialog(self, message, detailmessage):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setDetailedText(detailmessage)
        msg.setWindowTitle("提示信息")
        msg.exec_()


if __name__ == '__main__':
    client = Client()
    client.run()
