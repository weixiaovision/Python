#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import view
import os
from shutil import copy2, rmtree
import zipfile


class MainWindow(QMainWindow, view.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.old_version = None
        self.new_version = None
        self.svn_path = None
        self.output_path = None
        self.diff_file_list = []

    def run(self):
        self.view.opendirPushButton.clicked.connect(self.select_dir)
        self.view.outputPushButton.clicked.connect(self.select_out_dir)
        self.view.oldPushButton.clicked.connect(self.select_file)
        self.view.newPushButton.clicked.connect(self.select_new_file)
        self.view.startPushButton.clicked.connect(self.insert_listwidget)
        self.view.copyPushButton.clicked.connect(self.copy_start)
        self.view.checkPushButton.clicked.connect(self.get_diff_zip)
        self.view.show()
        sys.exit(self.app.exec_())

    def readconfig(self):
        if os.path.exists('path.conf'):
            f = open('path.conf', 'r')
            pathlist = f.readlines
            self.view.pathLineEdit.setText(pathlist[0])
            self.view.outputLineEdit.setText(pathlist[1])
            f.close()

    def insert_listwidget(self):
        self.diff_file_list = []
        self.get_version_path()
        if not self.old_version or not self.new_version:
            self.showdialog('输入框不能为空')
            return
        if not os.path.exists(self.svn_path):
            self.showdialog('svn路径不存在')
            return
        modify, add, delete = self.getfilelist(self.old_version, self.new_version, self.svn_path)
        modify.reverse()
        add.reverse()
        delete.reverse()
        self.diff_file_list.extend(modify)
        self.diff_file_list.extend(add)
        self.view.modifyTextEdit.setText(modify)
        self.view.addTextEdit.setText(add)
        self.view.deleteTextEdit.setText(delete)
        self.view.copyPushButton.setEnabled(True)
        self.view.checkPushButton.setEnabled(True)

    def copy_start(self):
        if not os.path.exists(self.output_path):
            self.showdialog('输出目录文件夹不存在')
            return
        modify, add, delete = self.getfilelist(self.old_version, self.new_version, self.svn_path, False)
        print('开始更新到版本：%s' % self.new_version)
        os.system('svn update -r %s %s' % (self.new_version, self.svn_path))
        outputpath = os.path.join(self.output_path, self.new_version)
        if len(modify) > 0:
            print('开始拷贝%s改动文件，总计：%d' % (self.new_version, len(modify)))
            self.copy_file_list(self.svn_path, outputpath, modify)
        if len(add) > 0:
            print('开始拷贝%s改动文件，总计：%d' % (self.new_version, len(add)))
            self.copy_file_list(self.svn_path, outputpath, add)
        print('开始更新到版本：%s' % self.old_version)
        os.system('svn update -r %s %s' % (self.old_version, self.svn_path))
        oldoutpath = os.path.join(self.output_path, self.old_version)
        if len(modify) > 0:
            print('开始拷贝版本%s的改动文件，总计：%d' % (self.old_version, len(modify)))
            self.copy_file_list(self.svn_path, oldoutpath, modify)
        if len(delete) > 0:
            print('开始拷贝版本%s的删除了的文件，总计：%d' % (self.old_version, len(delete)))
            self.copy_file_list(self.svn_path, oldoutpath, delete)
        # 写入配置文件
        f = open('path.conf', 'w')
        f.writelines([self.svn_path, self.output_path])
        f.close()

    # def clear(self):
    #     self.view.modifyListWidget.clear()
    #     self.view.addListWidget.clear()
    #     self.view.deleteListWidget.clear()

    def getfilelist(self, old_version, new_version, path, istrue=True):
        modify_file_list = []
        add_file_list = []
        delete_file_list = []
        modify_file_list_path = []
        add_file_list_path = []
        delete_file_list_path = []
        text = None
        try:
            r = os.popen('svn diff -r %s:%s --summarize %s' % (old_version, new_version, path))
            text = r.readlines()
        except Exception as e:
            self.showdialog('svn查询失败', e)
        for line in text:
            linesplitlist = line.split()
            if linesplitlist[0] == 'M':
                modify_file_list.append(linesplitlist[1].split('Resource')[1].replace('\\', '/'))
                modify_file_list_path.append(linesplitlist[1].replace('\\', '/'))
            elif linesplitlist[0] == 'A':
                add_file_list.append(linesplitlist[1].split('Resource')[1].replace('\\', '/'))
                add_file_list_path.append(linesplitlist[1].replace('\\', '/'))
            else:
                delete_file_list.append(linesplitlist[1].split('Resource')[1].replace('\\', '/'))
                delete_file_list_path.append(linesplitlist[1].replace('\\', '/'))
        if istrue:
            return modify_file_list, add_file_list, delete_file_list
        return modify_file_list_path, add_file_list_path, delete_file_list_path

    def get_version_path(self):
        self.old_version = self.view.oldversionLineEdit.text()
        self.new_version = self.view.newversionLineEdit.text()
        self.svn_path = self.view.pathLineEdit.text()
        self.output_path = self.view.outputLineEdit.text()

    # 拷贝文件
    def copy_file_list(self, svn_path, outputpath, file_list):
        # 清空文件夹
        rmtree(outputpath)
        for path in file_list:
            print(path)
            new_path = path.replace(svn_path, outputpath)
            print(new_path)
            if not os.path.exists(os.path.split(new_path)[0]):
                os.makedirs(os.path.split(new_path)[0])
            if os.path.isfile(path):
                copy2(path, new_path)

    def select_dir(self):
        msg = QFileDialog()
        dir_select = msg.getExistingDirectory()
        if dir_select:
            self.view.pathLineEdit.setText(dir_select)

    def select_out_dir(self):
        msg = QFileDialog()
        dir_select = msg.getExistingDirectory()
        if dir_select:
            self.view.outputLineEdit.setText(dir_select)

    def select_file(self):
        msg = QFileDialog()
        file_select = msg.getOpenFileName()
        print(file_select)
        if file_select:
            self.view.oldLineEdit.setText(file_select[0])

    def select_new_file(self):
        msg = QFileDialog()
        file_select = msg.getOpenFileName()
        if file_select:
            self.view.newLineEdit.setText(file_select[0])

    def get_diff_zip(self):
        old_file_list = zipfile.ZipFile(self.view.oldLineEdit.text()).namelist()
        new_file_list = zipfile.ZipFile(self.view.newLineEdit.text()).namelist()
        diff_zip_file = list(set(new_file_list).difference(set(old_file_list)))
        for file in self.diff_file_list:
            if file not in new_file_list:
                print('漏更新：%s' % file)
        for file in diff_zip_file:
            if file not in self.diff_file_list:
                print('多更新文件：%s' % file)

    # 弹框提示
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
