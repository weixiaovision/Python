#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os
import sys
from tkinter import *
import configparser
import codecs
import pymysql.cursors
from tkinter import Tk, StringVar, ttk
if not sys.version_info[0] == 3:
    print("this script on run under python3.x")
    os.system("pause")
    sys.exit()


class MainWindow:
    host = ''
    username = ''
    password = ''
    port = 0
    db = ''
    coon = None
    jumplist = None
    cf = None

    def __init__(self):
        self.frame = Tk()
        self.frame.title('活动查看日志')
        self.frame.geometry('1100x1100')
        self.frame.resizable(width=True, height=True)  # 宽不可变, 高可变,默认为True
        self.frame.minsize(100, 150)
        self.cf = self.read_config_jump('jumplist.conf')


        self.server = StringVar()
        # self.datas = StringVar()
        self.name = StringVar()
        self.describe = StringVar()
        self.time = StringVar()
        self.condition = StringVar()
        self.pic = StringVar()
        self.actpic = StringVar()
        self.reward = StringVar()
        self.actdes = StringVar()
        self.actID =StringVar()
        self.item = StringVar()
        self.itemid = StringVar()

        self.label = Label(self.frame, text='数据库')
        self.box = ttk.Combobox(self.frame, textvariable=self.server, state='readonly')
        self.box['values'] = self.read_config_sections('server.conf')
        self.box.current(0)
        # self.button = Button(self.frame, text='连接数据库', command=self.test)

        self.label.grid(row=0, column=1)
        self.box.grid(row=0, column=2)
        # self.button.grid(row=0, column=3)

        self.label10 = Label(self.frame, text='活动关键字')
        self.Lb2 = Listbox(self.frame, width=100, height=4, bg='#BFEFFF')
        self.entry10 = Entry(self.frame, textvariable=self.actdes, width=100, bg='#C1FFC1')
        self.button2 = Button(self.frame, text='查询')
        # self.button2.bind('<Return>', self.select_actid)
        # self.button2.focus_get()
        self.Lb2.grid(row=2, column=2)
        self.entry10.grid(row=1, column=2)
        self.button2.grid(row=1, column=3)
        self.label10.grid(row=1, column=1)
        self.Lb2.bind('<<ListboxSelect>>', self.click_button)

        self.label1 = Label(self.frame, text='活动ID')
        self.entry1 = Entry(self.frame, textvariable=self.actID, width=100, bg='#C1FFC1')
        self.button1 = Button(self.frame, text='查询', command=self.select)

        self.label1.grid(row=3, column=1)
        self.entry1.grid(row=3, column=2)
        self.button1.grid(row=3, column=3)
        self.label2 = Label(self.frame, text='查询结果')
        self.label2.grid(row=4, column=1)
        # self.entry2 = Entry(self.frame, textvariable=self.datas)

        # self.entry2.grid(row=2, column=2)
        self.label3 = Label(self.frame, text='活动名称')
        self.entry3 = Entry(self.frame, textvariable=self.name, width=100, bg='#BFEFFF')
        self.label3.grid(row=4, column=1)
        self.entry3.grid(row=4, column=2)

        self.label4 = Label(self.frame, text='活动描述')
        self.entry4 = Entry(self.frame, textvariable=self.describe, width=100, bg='#C1FFC1')
        self.label4.grid(row=5, column=1)
        self.entry4.grid(row=5, column=2)

        self.label5 = Label(self.frame, text='活动时间')
        self.entry5 = Entry(self.frame, textvariable=self.time, width=100, bg='#BFEFFF')
        self.label5.grid(row=6, column=1)
        self.entry5.grid(row=6, column=2)

        self.label6 = Label(self.frame, text='参与条件')
        self.entry6 = Entry(self.frame, textvariable=self.condition,  width=100, bg='#C1FFC1')
        self.label6.grid(row=7, column=1)
        self.entry6.grid(row=7, column=2)

        self.label7 = Label(self.frame, text='跳转界面')
        self.entry7 = Entry(self.frame, textvariable=self.pic, width=100, bg='#BFEFFF')
        self.label7.grid(row=8, column=1)
        self.entry7.grid(row=8, column=2)

        # self.label8 = Label(self.frame, text='活动中心图')
        # self.entry8 = Entry(self.frame, textvariable='暂未查询', width=100)
        # self.label8.grid(row=7, column=1)
        # self.entry8.grid(row=7, column=2)

        self.label9 = Label(self.frame, text='描述条件奖励')
        self.Lb1 = Listbox(self.frame, width=100, bg='#C1FFC1')
        self.Lb1.grid(row=9, column=2)
        self.label9.grid(row=9, column=1)
        # self.box9.grid(row=9, column=2)

        self.label11 = Label(self.frame, text='关键字')
        self.Lb3 = Listbox(self.frame, width=100, height=4, bg='#BFEFFF')
        self.entry11 = Entry(self.frame, textvariable=self.item, width=100, bg='#C1FFC1')
        self.button3 = Button(self.frame, text='模糊搜索', command=self.select_item)
        self.Lb3.grid(row=11, column=2)
        self.entry11.grid(row=10, column=2)
        self.button3.grid(row=10, column=3)
        self.label11.grid(row=10, column=1)
        # self.Lb3.bind('<<ListboxSelect>>', self.click_button)
        self.Lb3.bind('<<ListboxSelect>>', self.click_button_item)

        self.label12 = Label(self.frame, text='宝箱ID')
        self.entry12 = Entry(self.frame, textvariable=self.itemid, width=100, bg='#C1FFC1')
        self.button4 = Button(self.frame, text='查询', command=self.select_box)
        self.label12.grid(row=12, column=1)
        self.entry12.grid(row=12, column=2)
        self.button4.grid(row=12, column=3)

        self.Lb4 = Listbox(self.frame, width=100, height=10, bg='#BFEFFF')
        self.Lb4.grid(row=13, column=2)
# 选中活动列表中活动触发事件

    def click_button(self, event):
        if len(self.Lb2.curselection()) != 0:
            self.actID.set(self.Lb2.get(self.Lb2.curselection())[1])
            self.select()

# 选中宝箱列表中宝箱ID触发事件

    def click_button_item(self, event):
        if len(self.Lb3.curselection()) != 0:
            self.itemid.set(self.Lb3.get(self.Lb3.curselection())[1])
            # self.select()

    def run(self):
        self.frame.mainloop()

    def read_config_jump(self, config_path):
        cf = configparser.ConfigParser()
        cf.read_file(codecs.open(config_path, 'r', 'utf-8'))
        return cf

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

# 连接数据库
    def connect_db(self):
        if self.box.get():
            self.read_config_sections('server.conf', self.box.get())
        else:
            print('请选择正确的数据库地址')
            return
        try:
            self.coon = pymysql.connect(host=self.host,
                                        user=self.user,
                                        port=self.port,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8'
                                        )
        except Exception as e:
            print(e)
            print('连接数据库失败')
            sys.exit()

# 查询活动数据
    def select(self, args=None):
        activityID = None
        if self.Lb1.size() != 0:
            self.Lb1.delete(0, self.Lb1.size())
        if self.entry1.get():
            activityID = self.entry1.get()
        else:
            print('请输入活动ID')
            return
        sql_name = 'select Heading from t_s_activity_performance where ID=%s' % activityID
        sql_describe = 'select RuleShow from t_s_activity_performance where ID=%s' % activityID
        sql_time = 'select BeginTime,EndTime from t_s_activity where ID=%s' % activityID
        sql_condition = 'select cond from t_s_activity where ID=%s' % activityID
        sql_pic = 'select jumpaddress from t_s_activity_performance where ID=%s' % activityID
        sql_actpic = ''
        sql_reward = 'select reward from t_s_activity_task where ActivityId=%s' % activityID
        sql_comment = 'select Comment, State from t_s_activity_task where ActivityId=%s' % activityID

        cursor = None
        try:
            self.connect_db()
            cursor = self.coon.cursor()
            cursor.execute(sql_name, args)
            name = cursor.fetchall()
            self.name.set(name)
            cursor.execute(sql_describe)
            describe = cursor.fetchall()
            if describe[0][0] != '':
                self.describe.set(describe)
            else:
                self.describe.set('没有配置活动描述')
            cursor.execute(sql_time)
            time = cursor.fetchall()
            self.time.set(time[0][0] + ' -> ' + time[0][1])
            cursor.execute(sql_condition)
            condition = cursor.fetchall()
            self.condition.set(condition)
            cursor.execute(sql_pic)
            pic = cursor.fetchall()
            if pic[0][0] != '0':
                pic_jieshi = self.cf.get('jumplist', pic[0][0])
                self.pic.set(pic[0][0] + '  ' + pic_jieshi)
            else:
                self.pic.set('没有配置跳转图')
            cursor.execute(sql_reward)
            rewards = cursor.fetchall()
            cursor.execute(sql_comment)
            comment = cursor.fetchall()
            rewards_list = []
            for reward in rewards:
                rewards_list.append(reward[0])

            if len(rewards) != 0:
                name_list = []
                for reward in rewards_list:
                    for reward_1 in reward.split('|'):
                        cursor.execute('select name from t_s_item where ID=%s' % reward_1.split(',')[0])
                        name_1 = cursor.fetchall()[0][0]
                        reward = reward.replace(reward_1.split(',')[0], name_1)
                    name_list.append(reward)
                name_list_2 = []
                for i in range(len(name_list)):
                    if list(list(comment[i]))[1] == '':
                        name_list_2.append(list(list(comment[i]))[0] + '   ' + '没有配置state' + '   ' + name_list[i])
                    else:
                        name_list_2.append(list(list(comment[i]))[0] + '   ' + list(list(comment[i]))[1] + '   ' + name_list[i])
                for i in range(len(name_list_2)):
                    self.Lb1.insert(i, name_list_2[i])
            else:
                pass
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()

# 模糊搜索活动
    def select_actid(self, event):
        actdes = None
        if self.Lb2.size() != 0:
            self.Lb2.delete(0, self.Lb2.size())
        if self.entry10.get():
            actdes = self.entry10.get().strip()
        else:
            print('请输入活动关键字')
            return
        sql_act = 'select Heading, ID from t_s_activity_performance where Heading LIKE "%{abc}%"'.format(abc=actdes)

        cursor = None
        try:
            self.connect_db()
            cursor = self.coon.cursor()
            cursor.execute(sql_act, args)
            names = cursor.fetchall()
            list_activityID_nosame = []
            list_activityID = []
            # 兼容搜索不到的活动
            if len(names) == 0:
                self.Lb2.insert(0, '无此类活动')
            else:
                for name in names:
                    # 去除重复的活动ID
                    if name[1] not in list_activityID:
                        list_activityID.append(name[1])
                        list_activityID_nosame.append(name)
                for i in range(len(list_activityID_nosame)):
                    self.Lb2.insert(i, list_activityID_nosame[i])
        except Exception as e:
            print(e)
            print('链接服务器失败')
        finally:
            if cursor:
                cursor.close()

    def select_item(self, args=None):
        itemname = None
        if self.Lb3.size() != 0:
            self.Lb3.delete(0, self.Lb3.size())
        if self.entry11.get():
            itemname = self.entry11.get()
        else:
            print('请输入item关键字')
            return
        sql_item = 'select Name, ID from t_s_item where NAME LIKE "%{abc}%"'.format(abc=itemname)
        cursor = None
        try:
            self.connect_db()
            cursor = self.coon.cursor()
            cursor.execute(sql_item, args)
            names = cursor.fetchall()
            if len(names) == 0:
                self.Lb3.insert(0, '无此类物品')
            for i in range(len(names)):
                self.Lb3.insert(i, names[i])
        except Exception as e:
            print(e)
            print('链接服务器失败')
        finally:
            if cursor:
                cursor.close()

    def select_box(self, args=None):
        itemid = None
        if self.Lb4.size() != 0:
            self.Lb4.delete(0, self.Lb4.size())
        if self.entry12.get():
            itemid = self.entry12.get()
        else:
            print('请输入宝箱ID')
            return
        sql_box = 'SELECT DropGroup,ItemName,ItemCount,ItemWeight FROM t_s_reward_missionitem WHERE DropID in (SELECT TargetID FROM t_s_item where id = %s)' % itemid

        cursor = None
        try:
            self.connect_db()
            cursor = self.coon.cursor()
            cursor.execute(sql_box)
            box_item = cursor.fetchall()
            # 过滤掉权重为0的物品
            box_item_list = []
            for item in box_item:
                if item[-1] != 0:
                    box_item_list.append(list(item))
            print(box_item_list)
            # 根据dropgroup分组
            dropgroup_list = []
            for item in box_item_list:
                if item[0] not in dropgroup_list:
                    dropgroup_list.append(item[0])
            print(dropgroup_list)
            dropgroup_list_item = [list() for i in range(len(dropgroup_list))]
            print(dropgroup_list_item)
            i = 0
            for dropgroup in dropgroup_list:
                for item in box_item_list:
                    print(item)
                    if dropgroup == item[0]:
                        dropgroup_list_item[i].append(item)
                i += 1
            print(dropgroup_list_item)
            print('============')


            # 分组计算权重
            item_weight_add_list = []
            for group in dropgroup_list_item:
            # 获取权重总值
                item_weight_add = 0
                for item in group:
                    item_weight_add += int(item[-1])
                item_weight_add_list.append(item_weight_add)
            print(item_weight_add_list)

            # 列表中加上权重百分比
            item_weight = []
            for weight in item_weight_add_list:
                for item in box_item_list:
                    item_baifen = str(round(int(item[-1])*100/weight, 2)) + '%'
                    item_weight.append(item + [item_baifen])
            print(item_weight)
            # for i in range(len(item_weight)):
            #     self.Lb4.insert(i, item_weight[i][3] + '    ' + item_weight[i][-1])
            # if len(rewards) != 0:
            #     name_list = []
            #     for reward in rewards_list:
            #         for reward_1 in reward.split('|'):
            #             cursor.execute('select name from t_s_item where ID=%s' % reward_1.split(',')[0])
            #             name_1 = cursor.fetchall()[0][0]
            #             reward = reward.replace(reward_1.split(',')[0], name_1)
            #         name_list.append(reward)
            #     name_list_2 = []
            #     for i in range(len(name_list)):
            #         if list(list(comment[i]))[1] == '':
            #             name_list_2.append(list(list(comment[i]))[0] + '   ' + '没有配置state' + '   ' + name_list[i])
            #         else:
            #             name_list_2.append(list(list(comment[i]))[0] + '   ' + list(list(comment[i]))[1] + '   ' + name_list[i])
            #     for i in range(len(name_list_2)):
            #         self.Lb1.insert(i, name_list_2[i])
            # else:
            #     pass
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()


if __name__ == '__main__':
    MainWindow = MainWindow()
    MainWindow.run()



