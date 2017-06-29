#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os
import sys
from tkinter import *
import configparser
import codecs
import pymysql.cursors
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mBox
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox as mBox
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
        self.frame.title('DDT测试工具')
        self.frame.geometry('900x600')
        self.frame.resizable(width=True, height=True)  # 宽不可变, 高可变,默认为True
        self.frame.minsize(100, 150)
        # 初始化
        # tab分页
        self.begin_end_time = StringVar()
        self.tabControl = None
        self.tab1 = None
        self.tab2 = None
        # 数据库combobox
        self.box = None
        # 活动名称
        self.heading = StringVar()
        self.name = StringVar()
        self.boxid = StringVar()

        self.createWidgets(self.frame)
        self.jumplist_cf = self.read_config_jump('jumplist.conf')
        self.jumplist_list = self.jumplist_cf.options('jumplist')
        self.frame.mainloop()

    # 初始化
        # tab分页
        self.tabControl = None
        self.tab1 = None
        self.tab2 = None
        # 数据库combobox
        self.box = None
        self.tree = None
        # 活动名称

    def createWidgets(self, master):
        self.tabControl = ttk.Notebook(master)  # Create Tab Control

        self.tab1 = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.tab1, text='活动快速查询')  # Add the tab
        self.create_tab1(self.tab1)

        self.tab2 = ttk.Frame(self.tabControl)  # Add a second tab
        self.tabControl.add(self.tab2, text='物品宝箱查询')  # Make second tab visible
        self.create_tab2(self.tab2)
        #
        # tab3 = ttk.Frame(tabControl)  # Add a third tab
        # tabControl.add(tab3, text='第三页')  # Make second tab visible
        #
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

    def create_tab2(self, master):
        self.monty_2 = ttk.LabelFrame(master)
        self.monty_2.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(self.monty_2, text='数据库').grid(row=0, column=1)
        self.box2 = ttk.Combobox(self.monty_2, state='readonly')
        self.box2['values'] = self.read_config_sections('server.conf')
        self.box2.current(0)
        # self.button = Button(self.frame, text='连接数据库', command=self.test)
        self.box2.grid(row=0, column=2, sticky='w', pady=10)
        ttk.Label(self.monty_2, text='物品关键字').grid(row=1, column=1)
        self.Lb_2 = Listbox(self.monty_2, width=30, height=4, bg='#BFEFFF')
        self.entry_2 = Entry(self.monty_2, textvariable=self.name, width=30, bg='#C1FFC1')
        self.button_2 = Button(self.monty_2, text='查询', command=self.select_item)
        self.entry_2.bind('<Return>', self.click_enter_2)
        self.entry_2.grid(row=1, column=2, sticky='w', pady=10)
        self.button_2.grid(row=1, column=3, sticky='w')
        self.Lb_2.grid(row=2, column=2, columnspan=3, sticky='w', pady=10)
        self.Lb_2.bind('<<ListboxSelect>>', self.click_button_item)

        ttk.Label(self.monty_2, text='宝箱ID').grid(row=3, column=1)
        self.entry_2_2 = Entry(self.monty_2, textvariable=self.boxid, width=30)
        self.button_2_2 =Button(self.monty_2, text='查询', command=self.select_box)
        self.entry_2_2.grid(row=3, column=2, sticky='w', pady=10)
        self.button_2_2.grid(row=3, column=3, sticky='w')

        self.tree4 = ttk.Treeview(self.monty_2, columns=('a', 'b', 'c', 'd', 'e'), height=10, show='headings')
        # 设置列宽
        self.tree4.column('a', width=100, anchor='center')
        self.tree4.column('b', width=200, anchor='center')
        self.tree4.column('c', width=100, anchor='center')
        self.tree4.column('d', width=100, anchor='center')
        self.tree4.column('e', width=100, anchor='center')
        # 设置列名
        self.tree4.heading('a', text='DropGroup')
        self.tree4.heading('b', text='ItemName')
        self.tree4.heading('c', text='ItemCount')
        self.tree4.heading('d', text='ItemWeight')
        self.tree4.heading('e', text='百分比')
        # self.tree4.bind("<Double-1>", self.OnDoubleClick)
        self.tree4.grid(row=4, column=2, columnspan=5, sticky='w', pady=10)


    def create_tab1(self, master):
        self.monty = ttk.LabelFrame(master)
        self.monty.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(self.monty, text='数据库').grid(row=0, column=1)
        self.box = ttk.Combobox(self.monty, state='readonly')
        self.box['values'] = self.read_config_sections('server.conf')
        self.box.current(0)
        # self.button = Button(self.frame, text='连接数据库', command=self.test)
        self.box.grid(row=0, column=2, sticky='w', pady=10)
        ttk.Label(self.monty, text='活动关键字').grid(row=1, column=1)
        self.Lb1 = Listbox(self.monty, width=40, height=4, bg='#BFEFFF')
        self.entry1 = Entry(self.monty, textvariable=self.heading, width=30, bg='#C1FFC1')
        self.button1 = Button(self.monty, text='查询', command=self.select_actid)
        self.button2 = Button(self.monty, text='清空关键字', command=self.reset_entry)
        self.entry1.bind('<Return>', self.click_enter)
        self.entry1.grid(row=1, column=2, sticky='w', pady=10)
        self.button1.grid(row=1, column=3, sticky='w')
        self.button2.grid(row=1, column=4)
        self.Lb1.grid(row=2, column=2, columnspan=2, sticky='w', pady=10)
        self.Lb1.bind('<<ListboxSelect>>', self.click_button)

        ttk.Label(self.monty, text='活动时间').grid(row=3, column=1)
        self.entry2 = ttk.Entry(self.monty, textvariable=self.begin_end_time, state='readonly', width=40)
        self.entry2.grid(row=3, column=2, columnspan=2, sticky='w', pady=10)
        # 第一列基本信息
        ttk.Label(self.monty, text='活动基本信息').grid(row=4, column=1)
        self.tree = ttk.Treeview(self.monty, columns=('Heading', 'Kind', 'TipsType', 'DetailType', 'MainPicture'), height=1, show='headings')
        # 设置列宽
        self.tree.column('Heading', width=200)
        self.tree.column('Kind', width=50, anchor='center')
        self.tree.column('TipsType', width=70, anchor='center')
        self.tree.column('DetailType', width=70, anchor='center')
        self.tree.column('MainPicture', width=300)
        # 设置列名
        self.tree.heading('Heading',    text='Heading')
        self.tree.heading('Kind',    text='Kind')
        self.tree.heading('TipsType',    text='TipsType')
        self.tree.heading('DetailType',    text='DetailType')
        self.tree.heading('MainPicture',    text='MainPicture')
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.grid(row=4, column=2, columnspan=3, sticky='w', pady=10)

        # 第二列基本信息
        self.tree2 = ttk.Treeview(self.monty, columns=('a', 'b', 'c', 'd'), height=1, show='headings')
        # 设置列宽
        self.tree2.column('a', width=200)
        self.tree2.column('b', width=200)
        self.tree2.column('c', width=200)
        self.tree2.column('d', width=100)
        # 设置列名
        self.tree2.heading('a', text='TimeShow')
        self.tree2.heading('b', text='RuleShow')
        self.tree2.heading('c', text='DetailRuleShow')
        self.tree2.heading('d', text='JumpAddress')
        self.tree2.bind("<Double-1>", self.OnDoubleClick_2)
        self.tree2.grid(row=5, column=2, columnspan=4, sticky='w', pady=10)

        ttk.Label(self.monty, text='活动描述奖励').grid(row=6, column=1)
        self.tree3 = ttk.Treeview(self.monty, columns=('a', 'b', 'c'), height=6, show='headings')
        # 设置列宽
        self.tree3.column('a', width=300)
        self.tree3.column('b', width=200)
        self.tree3.column('c', width=200)
        # 设置列名
        self.tree3.heading('a', text='Comment')
        self.tree3.heading('b', text='State')
        self.tree3.heading('c', text='Reward')
        self.tree3.bind("<Double-1>", self.OnDoubleClick_3)
        self.tree3.grid(row=6, column=2, columnspan=5, sticky='w', pady=10)

    def reset_entry(self):
        self.heading.set('')

    def click_enter(self, event):
        self.select_actid()

    def click_enter_2(self, event):
        self.select_item()


    def click_button_item(self, event):
        if len(self.Lb_2.curselection()) != 0:
            self.boxid.set(self.Lb_2.get(self.Lb_2.curselection())[1])
            self.select_box()

    def OnDoubleClick(self, event):
        selection = self.tree.selection()
        item = ttk.Treeview.item(self.tree, selection[0])['values']
        mBox.showinfo('详细信息', item[int(self.tree.identify_column(event.x)[1])-1])

    def OnDoubleClick_2(self, event):
        selection = self.tree2.selection()
        item = ttk.Treeview.item(self.tree2, selection[0])['values']
        mBox.showinfo('详细信息', item[int(self.tree2.identify_column(event.x)[1])-1])

    def OnDoubleClick_3(self, event):
        selection = self.tree3.selection()
        item = ttk.Treeview.item(self.tree3, selection[0])['values']
        mBox.showinfo('详细信息', item[int(self.tree3.identify_column(event.x)[1])-1])

# Lb1 绑定方法
    def click_button(self, event):
        if len(self.Lb1.curselection()) != 0:
            # self.actID.set(self.Lb2.get(self.Lb1.curselection())[1])
            self.select()

    # 读取跳转配置文件
    def read_config_jump(self, config_path):
        cf = configparser.ConfigParser()
        cf.read_file(codecs.open(config_path, 'r', 'utf-8'))
        return cf

    # 物品模糊搜索
    def select_item(self, args=None):
        itemname = None
        if self.Lb_2.size() != 0:
            self.Lb_2.delete(0, self.Lb_2.size())
        if self.entry_2.get():
            itemname = self.entry_2.get()
        else:
            mBox.showwarning('提示', '请输入item关键字')
        sql_item = 'select Name, ID from t_s_item where NAME LIKE "%{abc}%"'.format(abc=itemname)
        cursor = None
        try:
            self.connect_db(self.box2.get())
            cursor = self.coon.cursor()
            cursor.execute(sql_item, args)
            names = cursor.fetchall()
            if len(names) == 0:
                self.Lb_2.insert(0, '无此类物品')
            for i in range(len(names)):
                self.Lb_2.insert(i, names[i])
        except Exception as e:
            mBox.showwarning('提示', e)
        finally:
            if cursor:
                cursor.close()
            self.coon.close()

    # 活动查询主函数
    def select(self, args=None):
        # 清除上次查询结果
        tree_item = self.tree.get_children()
        if len(tree_item) > 0:
            for item in tree_item:
                self.tree.delete(item)
        tree2_item = self.tree2.get_children()
        if len(tree2_item) > 0:
            for item in tree2_item:
                self.tree2.delete(item)
        tree3_item = self.tree3.get_children()
        if len(tree3_item) > 0:
            for item in tree3_item:
                self.tree3.delete(item)
        activityID = None
        # if self.Lb1.size() == 0:
        #     return
        # 兼容点击无搜索活动
        if self.Lb1.get(self.Lb1.curselection()) == '无此类活动':
            return
        activityID = self.Lb1.get(self.Lb1.curselection())[1]
        sql_time = 'select BeginTime,EndTime from t_s_activity where ID=%s' % activityID
        sql_mes = 'select Heading,kind,tipstype,detailtype,mainpicture from t_s_activity_performance where ID =%s' % activityID
        sql_mes_2 = 'select TimeShow,RuleShow,DetailRuleShow,JumpAddress from t_s_activity_performance where ID =%s' % activityID
        sql_reward = 'select reward from t_s_activity_task where ActivityId=%s' % activityID
        sql_comment = 'select Comment, State from t_s_activity_task where ActivityId=%s' % activityID
        cursor = None
        try:
            self.connect_db(self.box.get())
            cursor = self.coon.cursor()
            cursor.execute(sql_time, args)
            time = cursor.fetchall()
            self.begin_end_time.set(time[0][0] + ' -> ' + time[0][1])

            cursor.execute(sql_mes, args)
            mes = cursor.fetchall()
            self.tree.insert('', 'end', values=mes[0])

            cursor.execute(sql_mes_2, args)
            mes_2 = cursor.fetchall()
            # 获取跳转图
            if mes_2[0][3] in self.jumplist_list:
                pic = self.jumplist_cf.get('jumplist', mes_2[0][3])
            # 替换掉跳转ID
                new_list = list(mes_2[0])
                new_list.pop(3)
                new_list += [pic]
                self.tree2.insert('', 'end', values=new_list)
            else:
                self.tree2.insert('', 'end', values=mes_2[0])
                mBox.showwarning('添加新的jumpaddress', '%s在jumplist.conf中没有找到，请在jumplist.conf中手动添加' % mes_2[0][3])

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
                        name_2 = cursor.fetchall()
                        if len(name_2) == 0:
                            mBox.showwarning('道具不存在提示', 'item表中无此道具：%s，通知策划在t_s_item中添加此物品' % reward_1.split(',')[0])
                            return
                        name_1 = name_2[0][0]
                        reward = reward.replace(reward_1.split(',')[0], name_1)
                    name_list.append(reward)
                name_list_2 = []
                for i in range(len(name_list)):
                    if list(list(comment[i]))[1] == '':
                        name_list_2.append(list(list(comment[i]))[0] + '   ' + '没有配置state' + '   ' + name_list[i])
                    else:
                        name_list_2.append(
                            list(list(comment[i]))[0] + '   ' + list(list(comment[i]))[1] + '   ' + name_list[i])
                for item in name_list_2:
                    self.tree3.insert('', 'end', values=item)

        except Exception as e:
            mBox.showwarning('Python Message Warning Box', e)

        finally:
            if cursor:
                cursor.close()
            self.coon.close()

# 读取数据库列表配置
    def read_config_sections(self, config_path, section=None):
        cf = configparser.ConfigParser()
        cf.read_file(codecs.open(config_path, 'r', 'utf-8'))
        if not section:
            return cf.sections()
        else:
            values = cf.items(section)
            self.host = values[0][1]
            self.port = int(values[1][1])
            self.username = values[2][1]
            self.password = values[3][1]
            self.db = values[4][1]

# 连接数据库
    def connect_db(self, sqladd):
        if sqladd:
            self.read_config_sections('server.conf', sqladd)
        else:
            mBox.showwarning('请选择正确的数据库地址')
            return
        try:
            self.coon = pymysql.connect(host=self.host,
                                        user=self.username,
                                        port=self.port,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8'
                                        )
        except Exception as e:
            mBox.showwarning('Python Message Warning Box', '数据库连接失败，请检查配置文件或者网络')

    def select_actid(self, args=None):
        actdes = None
        if self.Lb1.size() != 0:
            self.Lb1.delete(0, self.Lb1.size())
        if self.entry1.get():
            actdes = self.entry1.get().strip()
        else:
            mBox.showwarning('Python Message Warning Box', '请输入活动名称')
            return
        sql_act = 'select Heading, ID from t_s_activity_performance where Heading LIKE "%{abc}%"'.format(abc=actdes)

        cursor = None
        try:
            self.connect_db(self.box.get())
            cursor = self.coon.cursor()
            cursor.execute(sql_act, args)
            names = cursor.fetchall()
            list_activityID_nosame = []
            list_activityID = []
            # 兼容搜索不到的活动
            if len(names) == 0:
                self.Lb1.insert(0, '无此类活动')
            else:
                for name in names:
                    # 去除重复的活动ID
                    if name[1] not in list_activityID:
                        list_activityID.append(name[1])
                        list_activityID_nosame.append(name)
                for i in range(len(list_activityID_nosame)):
                    self.Lb1.insert(i, list_activityID_nosame[i])
        except Exception as e:
            mBox.showwarning('Python Message Warning Box', e)
        finally:
            if cursor:
                cursor.close()
            self.coon.close()

    def select_box(self, args=None):
        tree_item = self.tree4.get_children()
        if len(tree_item) > 0:
            for item in tree_item:
                self.tree4.delete(item)
        itemid = None
        if self.entry_2_2.get():
            itemid = self.entry_2_2.get()
        else:
            mBox.showwarning('提示信息', '请输入宝箱ID')
        sql_box = 'SELECT DropGroup,ItemName,ItemCount,ItemWeight FROM t_s_reward_missionitem WHERE DropID in (SELECT TargetID FROM t_s_item where id = %s)' % itemid

        cursor = None
        try:
            self.connect_db(self.box2.get())
            cursor = self.coon.cursor()
            cursor.execute(sql_box)
            box_item = cursor.fetchall()
            if not len(box_item):
                self.tree4.insert('', 'end', values='此物品不是宝箱')
                return
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
                    item_baifen = str(round(int(item[-1])*100/weight, 2)) + '%'
                    item_weight.append(item + [item_baifen])
                j += 1
            for item in item_weight:
                self.tree4.insert('', 'end', values=item)
        except Exception as e:
            mBox.showwarning('提示', e)
        finally:
            if cursor:
                cursor.close()
            self.coon.close()
if __name__ == '__main__':
    MainWindow()
