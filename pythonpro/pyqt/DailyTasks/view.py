# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dailytask.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.taskTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.taskTableWidget.setGeometry(QtCore.QRect(50, 80, 1101, 451))
        self.taskTableWidget.setObjectName("taskTableWidget")
        self.taskTableWidget.setColumnCount(5)
        self.taskTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.taskTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(4, item)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1020, 40, 101, 32))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 30, 571, 42))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addPushButton = QtWidgets.QPushButton(self.widget)
        self.addPushButton.setObjectName("addPushButton")
        self.horizontalLayout_2.addWidget(self.addPushButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nameLineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLineEdit.sizePolicy().hasHeightForWidth())
        self.nameLineEdit.setSizePolicy(sizePolicy)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout.addWidget(self.nameLineEdit)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "每日任务"))
        item = self.taskTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "日期"))
        item = self.taskTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "任务详细描述"))
        item = self.taskTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "完成进度"))
        item = self.taskTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "负责人"))
        self.pushButton.setText(_translate("MainWindow", "立即推送"))
        self.addPushButton.setText(_translate("MainWindow", "新增任务"))
        self.label.setText(_translate("MainWindow", "英文名"))
        self.checkBox.setText(_translate("MainWindow", "是否开启推送"))
        self.label_2.setText(_translate("MainWindow", "推送时间间隔"))
        self.comboBox.setToolTip(_translate("MainWindow", "分钟为单位"))
        self.comboBox.setItemText(0, _translate("MainWindow", "15"))
        self.comboBox.setItemText(1, _translate("MainWindow", "30"))
        self.comboBox.setItemText(2, _translate("MainWindow", "45"))
        self.comboBox.setItemText(3, _translate("MainWindow", "60"))
        self.comboBox.setItemText(4, _translate("MainWindow", "120"))
        self.taskTableWidget.setColumnWidth(1, 20)
        self.taskTableWidget.setColumnWidth(2, 663)
        self.taskTableWidget.setColumnWidth(4, 200)

