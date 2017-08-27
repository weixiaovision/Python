#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import view
import os
import xml.etree.ElementTree as ET


class MainWindow(QMainWindow, view.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.path_list = self.readconfig()

    def run(self):
        self.view.startPushButton.connect(self.start())
        self.view.show()
        sys.exit(self.app.exec_())

    def write(self, path, widget):
        text = os.popen('svn log -l 5 %s' % path).readlines()
        widget.setText(text)
        # 控制滚动条位置
        widget.verticalScrollBar().setValue(0)

    def start(self):
        self.out_diff()
        self.out_log()

    def out_log(self):
        self.write(self.path_list[0], self.view.clientwTextEdit)
        self.write(self.path_list[1], self.view.clientdTextEdit)
        self.write(self.path_list[2], self.view.serverwTextEdit)
        self.write(self.path_list[3], self.view.serverdTextEdit)
        self.write(self.path_list[4], self.view.tablewTextEdit)
        self.write(self.path_list[5], self.view.tabledTextEdit)

    def out_diff(self):
        self.view.clientdiffListWidget.clear()
        self.view.serverdiffListWidget.clear()
        self.view.tableListWidget.clear()
        self.diff_file(self.path_list[0], self.path_list[1], self.view.clientdiffListWidget)
        self.diff_file(self.path_list[2], self.path_list[3], self.view.serverdiffListWidget)
        self.diff_file(self.path_list[4], self.path_list[5], self.view.tableListWidget)

    def diff_file(self, path_w, path_d, widget):
        r = os.popen('svn diff --summarize {0} {1}'.format(path_d, path_w))
        text = r.readlines()
        # 筛选掉文件夹名
        for line in text:
            linesplit = line.split()[1]
            if linesplit:
                if os.path.splitext(linesplit)[1]:
                    print(line)
                    widget.addItem(line)

    def readconfig(self):
        path_list = []
        tree = ET.parse(os.path.join(os.path.dirname(__file__), 'path.xml'))
        root = tree.getroot()
        for child in root:
            path_list.append(child.text)
        return path_list

if __name__ == '__main__':
    client = Client()
    client.run()
