# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startPushButton.setGeometry(QtCore.QRect(540, 0, 113, 32))
        self.startPushButton.setObjectName("startPushButton")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 40, 1131, 681))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 1081, 611))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.clientwTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.clientwTextEdit.setObjectName("clientwTextEdit")
        self.verticalLayout.addWidget(self.clientwTextEdit)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.clientdTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.clientdTextEdit.setObjectName("clientdTextEdit")
        self.verticalLayout_2.addWidget(self.clientdTextEdit)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.serverwTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.serverwTextEdit.setObjectName("serverwTextEdit")
        self.verticalLayout_3.addWidget(self.serverwTextEdit)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.serverdTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.serverdTextEdit.setObjectName("serverdTextEdit")
        self.verticalLayout_4.addWidget(self.serverdTextEdit)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.tablewTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.tablewTextEdit.setObjectName("tablewTextEdit")
        self.verticalLayout_5.addWidget(self.tablewTextEdit)
        self.horizontalLayout_9.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.tabledTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.tabledTextEdit.setObjectName("tabledTextEdit")
        self.verticalLayout_6.addWidget(self.tabledTextEdit)
        self.horizontalLayout_9.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 30, 1031, 581))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.clientdiffLlistWidget = QtWidgets.QListWidget(self.layoutWidget1)
        self.clientdiffLlistWidget.setObjectName("clientdiffLlistWidget")
        self.verticalLayout_8.addWidget(self.clientdiffLlistWidget)
        self.verticalLayout_11.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.serverdiffListWidget = QtWidgets.QListWidget(self.layoutWidget1)
        self.serverdiffListWidget.setObjectName("serverdiffListWidget")
        self.verticalLayout_9.addWidget(self.serverdiffListWidget)
        self.verticalLayout_11.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_10.addWidget(self.label_9)
        self.tableListWidget = QtWidgets.QListWidget(self.layoutWidget1)
        self.tableListWidget.setObjectName("tableListWidget")
        self.verticalLayout_10.addWidget(self.tableListWidget)
        self.verticalLayout_11.addLayout(self.verticalLayout_10)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startPushButton.setText(_translate("MainWindow", "开始"))
        self.label.setText(_translate("MainWindow", "客户端-w"))
        self.label_2.setText(_translate("MainWindow", "客户端-D"))
        self.label_3.setText(_translate("MainWindow", "服务器-w"))
        self.label_4.setText(_translate("MainWindow", "服务器-D"))
        self.label_5.setText(_translate("MainWindow", "数据表-w"))
        self.label_6.setText(_translate("MainWindow", "数据表-D"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "日志输出"))
        self.label_7.setText(_translate("MainWindow", "客户端差异列表"))
        self.label_8.setText(_translate("MainWindow", "服务器差异列表"))
        self.label_9.setText(_translate("MainWindow", "模板表差异列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "差异文件列表"))

