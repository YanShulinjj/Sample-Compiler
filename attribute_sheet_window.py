# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'voca.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor
import  pickle
from extract_word import parseString
import time


def transfer(data):
    '''
    :param data:  [dict]
    :return: [[]]， header
    '''

    r = []
    header = list(data[0].keys())
    for d in data:
        v = [d[h] for h in header]
        r.append(v)

    return r, header


class  Ui_AttributeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_AttributeWindow, self).__init__(parent)
        self.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(4)

        self.verticalLayout.addWidget(self.tableWidget)

        self.tableWidget.setColumnWidth(0, 40)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.resizeColumnToContents(0)
        # self.tableWidget.setHorizontalHeaderLabels(['单词','类别','所在行','所在列'])
        self.tableWidget.horizontalHeader().setResizeContentsPrecision(0)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "词汇表"))


    def insert_data_c(self):

        # data, errors = parseString(text)
        # print("data: ", data)
        # 从文件读出结果列表
        # time.sleep(5)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "常量属性表"))

        data = pickle.load(open('data/const_sheet.pkl', 'rb')) # 当前的data是 [dict] 形式的 需要转换
        print("data", data)
        data, header = transfer(data)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)
        for i in range(len(data)):
            for j in range(len(header)):
                item = QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i%2 == 0:
                    item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                else:
                    item.setBackground(QBrush(QColor(176, 196, 222)))
                self.tableWidget.setItem(i, j, item)
        self.show()

    def insert_data_v(self):

        # data, errors = parseString(text)
        # print("data: ", data)
        # 从文件读出结果列表
        # time.sleep(5)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "变量属性表"))
        data = pickle.load(open('data/var_sheet.pkl', 'rb'))  # 当前的data是 [dict] 形式的 需要转换
        print("data", data)
        data, header = transfer(data)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)
        for i in range(len(data)):
            for j in range(len(header)):
                item = QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i % 2 == 0:
                    item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                else:
                    item.setBackground(QBrush(QColor(176, 196, 222)))
                self.tableWidget.setItem(i, j, item)
        self.show()

    def insert_data_m(self):

        # data, errors = parseString(text)
        # print("data: ", data)
        # 从文件读出结果列表
        # time.sleep(5)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "中间代码"))
        fg, data = pickle.load(open('data/midway_sheet.pkl', 'rb'))  # 当前的data是 [dict] 形式的 需要转换
        if fg:
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(['OP', 'arg1', 'arg2', 'result'])
            for i in range(len(data)):
                for j in range(4):
                    item = QTableWidgetItem(str(data[i][j]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    if i % 2 == 0:
                        item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                    else:
                        item.setBackground(QBrush(QColor(176, 196, 222)))
                    self.tableWidget.setItem(i, j, item)
            self.show()


