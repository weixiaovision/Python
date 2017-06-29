#!/usr/bin/python3
# -*- coding: utf-8 -*-


import queue
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
import view
import configparser
import codecs
import pymysql.cursors
import requests


class MainWindow(QMainWindow, view.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.host = None
        self.port = None
        self.db = None
        self.user = None
        self.password = None
        self.db_game = None
        self.ip = None
        self.serverport = None
        self.jumplist_cf = self.read_config_jump('jumplist.conf')
        self.jumplist_list = self.jumplist_cf.options('jumplist')

    def run(self):
        self.insert_combobox()
        self.view.goodsLineEdit.returnPressed.connect(self.insert_goodslistwidget)
        self.view.nameLineEdit.returnPressed.connect(self.insert_namelistwidget)
        self.view.nickLineEdit.returnPressed.connect(self.insert_nicklistwidget)
        self.view.otherLineEdit.returnPressed.connect(self.sendothergm)
        self.view.goodsListWidget.itemClicked.connect(self.item_click)
        self.view.nameListWidget.itemClicked.connect(self.insert_nametablewidget)
        self.view.sendPushButton.clicked.connect(self.sendgm)
        self.view.comboBox.currentIndexChanged.connect(self.set_server_port)
        self.view.executePushButton.clicked.connect(self.sendothergm)
        self.view.show()
        sys.exit(self.app.exec_())

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
            self.db_game = values[5][1]
            self.ip = values[6][1]
            self.serverport =values[7][1]

    # 读取默认的服务器IP、端口
    def set_server_port(self):
        self.read_config_sections('server.conf', self.view.comboBox.currentText())
        self.view.ipLineEdit.setText(self.ip)
        self.view.portLineEdit.setText(self.serverport)

    # 连接数据库
    def connect_db(self, istrue=True):
        # self.read_config_sections('server.conf', self.view.comboBox.currentText())
        dbname = None
        if istrue:
            dbname = self.db
        else:
            dbname = self.db_game
        try:
            coon = pymysql.connect(host=self.host,
                                   user=self.user,
                                   port=self.port,
                                   password=self.password,
                                   db=dbname,
                                   charset='utf8'
                                   )
            return coon
        except Exception as e:
            self.showdialog('数据库连接失败', str(e))
            sys.exit()

    # 查询数据库
    def select(self, args=None, istrue=True):
        cursor = None
        result = None
        coon = None
        try:
            if istrue:
                coon = self.connect_db()
            else:
                coon = self.connect_db(False)
            cursor = coon.cursor()
            cursor.execute(args)
            result = cursor.fetchall()
            return result
        except Exception as e:
            self.showdialog('数据查询失败', str(e))
            sys.exit()
        finally:
            if cursor:
                cursor.close()
            coon.close()

    # 插入物品列表，item模糊搜索
    def insert_goodslistwidget(self):
        self.view.goodsListWidget.clear()
        namelike = self.view.goodsLineEdit.text()
        if namelike:
            result = self.select(
                'select ID,Name from t_s_item WHERE NAME like "%{abc}%"'.format(abc=namelike))
            if len(result) > 0:
                for item in result:
                    self.view.goodsListWidget.addItem(str(item[0]) + '  ' + item[1])
            else:
                self.view.goodsListWidget.addItem('查询结果为空')

    def insert_nicklistwidget(self):
        self.view.nickListWidget.clear()
        namelike = self.view.nickLineEdit.text()
        if namelike:
            result = self.select(
                'select NickName from t_u_player WHERE NickName like "%{0}%"'.format(namelike), False)
            if len(result) > 0:
                for item in result:
                    self.view.nickListWidget.addItem(item[0])
            else:
                self.view.nickListWidget.addItem('查询结果为空')

    # 开始查询主函数
    def item_click(self):
        id = None
        # 获取模糊搜索结果中选中的条目
        id_name = self.view.goodsListWidget.currentItem().text()
        if id_name:
            if len(id_name.split()) > 1:
                id = id_name.split()[0]
        if id:
            self.view.itemidLineEdit.setText(id)
            self.insert_goodstablewidget(id)
            self.insert_goods_tablewidget(id)

    # 插入到宝箱表格
    def insert_goods_tablewidget(self, itemid):
        sql_box = 'SELECT DropGroup,ItemName,ItemCount,ItemWeight FROM t_s_reward_missionitem ' \
                  'WHERE DropID in (SELECT TargetID FROM t_s_item where id = %s)' % itemid
        box_item = self.select(sql_box)
        # 过滤掉权重为0的物品
        box_item_list = []
        for item in box_item:
            if item[-1] != 0:
                box_item_list.append(list(item))
        # 根据dropgroup分组
        dropgroup_list = []
        for item in box_item_list:
            if item[0] not in dropgroup_list:
                dropgroup_list.append(item[0])
        dropgroup_list_item = [list() for i in range(len(dropgroup_list))]
        i = 0
        for dropgroup in dropgroup_list:
            for item in box_item_list:
                if dropgroup == item[0]:
                    dropgroup_list_item[i].append(item)
            i += 1

        # 分组计算权重
        item_weight_add_list = []
        for group in dropgroup_list_item:
            # 获取权重总值
            item_weight_add = 0
            for item in group:
                item_weight_add += int(item[-1])
            item_weight_add_list.append(item_weight_add)

        # 列表中加上权重百分比
        item_weight = []
        j = 0
        for weight in item_weight_add_list:
            for item in dropgroup_list_item[j]:
                item_baifen = str(round(int(item[-1]) * 100 / weight, 2)) + '%'
                item_weight.append(item + [item_baifen])
            j += 1

        # 插入表格
        self.view.goods_TableWidget.setRowCount(len(item_weight))
        k = 0
        for item1 in item_weight:
            for m in range(len(item1)):
                item = item1[m]
                item = QTableWidgetItem(str(item))
                self.view.goods_TableWidget.setItem(k, m, item)
            k += 1

    # 初始化db选择
    def insert_combobox(self):
        self.view.comboBox.addItems(self.read_config_sections('server.conf'))
        self.set_server_port()

    # 可能新宝箱奖励数据
    def insert_goodstablewidget(self, itemid):
        self.view.goodsTableWidget.setRowCount(0)
        itemlist_id = []
        namelist = []
        items = self.select('select param1, param2 from t_s_item where id = %s' % itemid)
        item = items[0][0]
        itemlist = item.split('|')
        for j in itemlist:
            itemlist_id.append(j.split(',')[0])
        if len(itemlist_id) > 1:
            self.view.goodsTableWidget.setRowCount(1)
            itemnames = self.select('select name from t_s_item where id in {0}'.format(tuple(itemlist_id)))
            for name in itemnames:
                namelist.append(name[0])
            newitem = self.new_replace(item, itemlist_id, namelist)
            self.view.goodsTableWidget.setItem(0, 0, QTableWidgetItem(newitem))
            self.view.goodsTableWidget.setItem(0, 1, QTableWidgetItem(str(items[0][1])))

    # 字符串列表替换
    def new_replace(self, str1, list1, list2):
        for i in range(len(list1)):
            str1 = str1.replace(list1[i], list2[i])
        return str1

    # 读取跳转配置文件
    def read_config_jump(self, config_path):
        cf = configparser.ConfigParser()
        cf.read_file(codecs.open(config_path, 'r', 'utf-8'))
        return cf

    # 弹框提示
    def showdialog(self, message, detailmessage=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        if detailmessage:
            msg.setDetailedText(detailmessage)
        msg.setWindowTitle("提示信息")
        msg.exec_()

    # 活动关键字搜索
    def insert_namelistwidget(self):
        self.view.nameListWidget.clear()
        namelike = self.view.nameLineEdit.text()
        if not namelike:
            self.showdialog('请输入活动关键字')
            return
        sql_act = 'select ID, Heading from t_s_activity_performance where Heading LIKE "%{0}%"'.format(namelike)
        names = self.select(sql_act)
        list_activityID_nosame = []
        list_activityID = []
        # 兼容搜索不到的活动
        if len(names) == 0:
            self.view.nameListWidget.addItem('没有此类活动')
        else:
            for name in names:
                # 去除重复的活动ID
                if name[0] not in list_activityID:
                    list_activityID.append(name[0])
                    list_activityID_nosame.append(name)
            for item in list_activityID_nosame:
                self.view.nameListWidget.addItem(str(item[0]) + '   ' + item[1])

    # 活动详细信息查询
    def insert_nametablewidget(self):
        self.view.msgTableWidget.setRowCount(0)
        self.view.msg_TableWidget.setRowCount(0)
        self.view.rewardTableWidget.setRowCount(0)
        activityID = self.view.nameListWidget.currentItem().text()
        if len(activityID.split()) == 1:
            return
        activityID = activityID.split()[0]
        sql_time = 'select BeginTime,EndTime from t_s_activity where ID=%s' % activityID
        sql_mes = 'select Heading,kind,tipstype,detailtype,mainpicture from t_s_activity_performance where ID =%s' % activityID
        sql_mes_2 = 'select TimeShow,RuleShow,DetailRuleShow,JumpAddress from t_s_activity_performance where ID =%s' % activityID
        sql_reward = 'select reward from t_s_activity_task where ActivityId=%s' % activityID
        sql_comment = 'select Comment, State, ExtraCond from t_s_activity_task where ActivityId=%s' % activityID
        sql_extra = 'select ExtraCond from t_s_activity_task where ActivityId=%s' % activityID
        time = self.select(sql_time)
        self.view.timeLineEdit.setText(time[0][0] + ' -> ' + time[0][1])
        mes = self.select(sql_mes)
        self.view.msgTableWidget.setRowCount(1)
        for i in range(len(mes[0])):
            item = QTableWidgetItem(str(mes[0][i]))
            self.view.msgTableWidget.setItem(0, i, item)

        mes_2 = self.select(sql_mes_2)
        # 获取跳转图
        if mes_2[0][3] in self.jumplist_list:
            pic = self.jumplist_cf.get('jumplist', mes_2[0][3])
            # 替换掉跳转ID
            new_list = list(mes_2[0])
            new_list.pop(3)
            new_list += [pic]
            self.view.msg_TableWidget.setRowCount(1)
            for i in range(len(new_list)):
                item = QTableWidgetItem(str(new_list[i]))
                self.view.msg_TableWidget.setItem(0, i, item)
        else:
            self.view.msg_TableWidget.setRowCount(1)
            for i in range(len(mes_2[0])):
                item = QTableWidgetItem(str(mes_2[0][i]))
                self.view.msg_TableWidget.setItem(0, i, item)
            self.showdialog('%s在jumplist.conf中没有找到，请在jumplist.conf中手动添加' % mes_2[0][3])

        comment = self.select(sql_comment)
        self.view.rewardTableWidget.setRowCount(len(comment))
        i = 0
        for item_1 in comment:
            for j in range(len(item_1)):
                item1 = QTableWidgetItem(item_1[j])
                self.view.rewardTableWidget.setItem(i, j, item1)
            i += 1
        rewards = self.select(sql_reward)
        rewards_list = []
        for reward in rewards:
            rewards_list.append(reward[0])
        name_list = []
        if len(rewards) != 0:
            for reward in rewards_list:
                for reward_1 in reward.split('|'):
                    if len(reward_1.split(',')) > 1:
                        name_2 = self.select('select name from t_s_item where ID=%s' % reward_1.split(',')[0])
                        if len(name_2) > 0:
                            name_1 = name_2[0][0]
                            reward = reward.replace(reward_1.split(',')[0], name_1)
                name_list.append(reward)
        for j in range(len(name_list)):
            self.view.rewardTableWidget.setItem(j, 3, QTableWidgetItem(name_list[j]))

        extra = self.select(sql_extra)
        extra_list = []
        for item3 in extra:
            extra_list.append(item3[0])
        name_list_1 = []
        if len(extra) != 0:
            for reward in extra_list:
                for reward_1 in reward.split('|'):
                    if len(reward_1.split(',')) > 1:
                        name_2 = self.select('select name from t_s_item where ID=%s' % reward_1.split(',')[0])
                        if len(name_2) > 0:
                            name_1 = name_2[0][0]
                            reward = reward.replace(reward_1.split(',')[0], name_1)
                name_list_1.append(reward)
        for j in range(len(name_list_1)):
            self.view.rewardTableWidget.setItem(j, 2, QTableWidgetItem(name_list_1[j]))

    # 发送GM命令
    def sendgm(self):
        result = None
        nickname = None
        if self.view.nickListWidget.currentItem():
            nickname = self.view.nickListWidget.currentItem().text()
        ip = self.view.ipLineEdit.text()
        port = self.view.portLineEdit.text()
        itemid = self.view.itemidLineEdit.text()
        count = self.view.countLineEdit.text()
        other = self.view.otherLineEdit.text()
        if not nickname:
            self.showdialog('请选择正确的昵称')
            return
        if not ip:
            self.showdialog('ip不能为空')
            return
        if not port:
            self.showdialog('port不能为空')
            return
        if not itemid:
            self.showdialog('ID不能为空')
            return
        if not count:
            self.showdialog('count不能为空')
            return
        try:
            response = requests.get('http://{0}:{1}/agent/testCommand?params={2}$item {3} {4}'
                                    .format(ip, port, nickname, itemid, count))
            result = response.text
        except Exception as e:
            self.showdialog('gm命令执行失败', str(e))
            return
        finally:
            if result:
                if result == 'testCommand success':
                    self.showdialog('GM命令执行成功')

    def sendothergm(self):
        result = None
        nickname = None
        if self.view.nickListWidget.currentItem():
            nickname = self.view.nickListWidget.currentItem().text()
        ip = self.view.ipLineEdit.text()
        port = self.view.portLineEdit.text()
        other = self.view.otherLineEdit.text()
        if not nickname:
            self.showdialog('请选择正确的昵称')
            return
        if not ip:
            self.showdialog('服务器ip不能为空')
            return
        if not port:
            self.showdialog('gm命令端口不能为空')
            return
        if not other:
            self.showdialog('命令不能为空')
            return
        try:
            response = requests.get('http://{0}:{1}/agent/testCommand?params={2}${3}'
                                    .format(ip, port, nickname, other))
            result = response.text
        except Exception as e:
            self.showdialog('gm命令执行失败', str(e))
            return
        finally:
            if result:
                if result == 'testCommand success':
                    self.showdialog('GM命令执行成功')


if __name__ == '__main__':
    client = Client()
    client.run()
