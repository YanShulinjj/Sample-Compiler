# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predictive_parsing.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from predict_analyze import Predict_Analyse, transfer, createPreAnalySheet, isLL1
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

def get_tem_smybol(grammar):
    '''
    提取所有终结符
    :param gammar:
    :return:
    '''
    res = []
    for l,r in grammar:
        for sign in r:
            if not sign[0].isupper():
                res.append(sign)
    return list(set(res))

def get_non_tem_smybol(grammar):
    '''
    提取所有非终结符
    :param gammar:
    :return:
    '''
    res = []
    for l,r in grammar:
        res.append(l)
    return list(set(res))

class Ui_MyPreAnalyseWindow(object):
    def setupUi(self, MyPreAnalyseWindow):
        MyPreAnalyseWindow.setObjectName("MyPreAnalyseWindow")
        MyPreAnalyseWindow.resize(800, 600)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(MyPreAnalyseWindow)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 9, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(MyPreAnalyseWindow)
        self.splitter.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grammar = QtWidgets.QTextEdit(self.groupBox)
        self.grammar.setObjectName("grammar")
        self.verticalLayout.addWidget(self.grammar)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sheet = QtWidgets.QTableWidget(self.groupBox_3)
        self.sheet.setObjectName("sheet")
        self.sheet.setColumnCount(0)
        self.sheet.setRowCount(0)
        self.horizontalLayout.addWidget(self.sheet)
        self.horizontalLayout_2.addWidget(self.splitter)
        self.splitter_2 = QtWidgets.QSplitter(MyPreAnalyseWindow)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.example = QtWidgets.QTextEdit(self.groupBox_2)
        self.example.setObjectName("example")
        self.verticalLayout_4.addWidget(self.example)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.groupBox_4 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.proeeed = QtWidgets.QTableWidget(self.groupBox_4)
        self.proeeed.setObjectName("proeeed")
        self.verticalLayout_6.addWidget(self.proeeed)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_6.addWidget(self.pushButton_3)
        # self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.verticalLayout_6.addWidget(self.pushButton_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2.addWidget(self.splitter_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 3)

        self.trigger()
        self.retranslateUi(MyPreAnalyseWindow)
        QtCore.QMetaObject.connectSlotsByName(MyPreAnalyseWindow)

    def retranslateUi(self, MyPreAnalyseWindow):
        _translate = QtCore.QCoreApplication.translate
        MyPreAnalyseWindow.setWindowTitle(_translate("MyPreAnalyseWindow", "LL1 Predictive Parsing"))
        self.groupBox.setTitle(_translate("MyPreAnalyseWindow", "Input LL1 grammar"))
        self.pushButton.setText(_translate("MyPreAnalyseWindow", "Built the Sheet"))
        self.groupBox_3.setTitle(_translate("MyPreAnalyseWindow", "Sheet Display"))
        self.groupBox_2.setTitle(_translate("MyPreAnalyseWindow", "Input the example"))
        self.pushButton_2.setText(_translate("MyPreAnalyseWindow", "Confirm"))
        self.groupBox_4.setTitle(_translate("MyPreAnalyseWindow", "Proceeding"))
        # item = self.proeeed.horizontalHeaderItem(0)
        # item.setText(_translate("MyPreAnalyseWindow", "Step"))
        # item = self.proeeed.horizontalHeaderItem(1)
        # item.setText(_translate("MyPreAnalyseWindow", "Stack"))
        # item = self.proeeed.horizontalHeaderItem(2)
        # item.setText(_translate("MyPreAnalyseWindow", "Input"))
        # item = self.proeeed.horizontalHeaderItem(3)
        # item.setText(_translate("MyPreAnalyseWindow", "Production"))
        self.pushButton_3.setText(_translate("MyPreAnalyseWindow", "Run by Step"))
        # self.pushButton_4.setText(_translate("MyPreAnalyseWindow", "Run"))

        self.init()


    def init(self):
        '''
        一些初始化工作
        :return:
        '''

        cols = ['Step', 'Stack', 'Input', 'Production']
        # self.proeeed.setVerticalHeaderLabels()
        self.proeeed.setRowCount(999)
        self.proeeed.verticalHeader().setVisible(False)
        self.proeeed.setColumnCount(len(cols))
        self.proeeed.setHorizontalHeaderLabels(cols)
        # self.sheet.setVerticalHeaderLabels(rows)
        self.proeeed.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proeeed.resizeColumnToContents(0)
        self.idx = 0
    def trigger(self):
        '''
        绑定事件
        :return:
        '''
        self.t = None
        s = '''
        S_->E
        E->TE'
        E'->+TE'
        E'->ε
        T->FT'
        T'->*FT'
        T'->ε
        F->(E)
        F->i 
        '''
        self.run_step_fg = True
        self.grammar.setText(s)
        self.pushButton.clicked.connect(self.built_sheet)  # 生成预测分析表
        self.pushButton_2.clicked.connect(self.confrim)  # 转化文法
        self.pushButton_3.clicked.connect(self.run_by_step)  # 一步一步的显示
        # self.pushButton_4.clicked.connect(self.run)  # 一次显示完

    def built_sheet(self):

        if self.grammar.isEnabled():
            self.pushButton.setText('Input new grammar')
            self.grammar.setEnabled(False)

        else:
            self.pushButton.setText('Bulid the sheet')
            self.grammar.setEnabled(True)


        s = self.grammar.toPlainText()
        # 设置语法输入栏不可修改
        print(s)

        self.g = transfer(s)

        if not isLL1(self.g):
            #清除表内数据
            self.sheet.clear()
            #弹出错误窗口
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'error',
                                'Is not LL1 grammar with begining at S_ !')
            self.grammar.setEnabled(True)
            self.pushButton.setText('Bulid the sheet')

        else:
            self.pre_sheet = createPreAnalySheet(self.g)

            # 显示在界面上
            rows = get_non_tem_smybol(self.g)
            cols = get_tem_smybol(self.g)+['#']
            if 'none' in cols:
                cols.remove('none')
            print(cols, rows)
            self.sheet.setRowCount(len(rows))
            self.sheet.setColumnCount(len(cols))
            self.sheet.setHorizontalHeaderLabels(cols)
            self.sheet.setVerticalHeaderLabels(rows)
            self.sheet.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.sheet.resizeColumnToContents(0)

            for i in range(len(rows)):
                for j in range(len(cols)):
                    print(rows[i])
                    key = rows[i]+'->'+cols[j]
                    print('KK', key)
                    if key in self.pre_sheet:
                        v = ''.join(self.pre_sheet[key])
                        if v == 'none':
                            v = 'ε'
                        item = QTableWidgetItem(v)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        if i % 2 == 0:
                            item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                        else:
                            item.setBackground(QBrush(QColor(176, 196, 222)))
                        self.sheet.setItem(i, j, item)

            print(self.pre_sheet)

    def confrim(self):
        print('hhhh')
        #重新打开run_tep
        self.run_step_fg = True
        self.proeeed.clearContents()
        if self.example.isEnabled():
            self.pushButton_2.setText('input an example')
            self.text = self.example.toPlainText()
            self.example.setEnabled(False)
        else:
            self.pushButton_2.setText('confirm')
            self.example.setEnabled(True)

    def run_by_step(self):
        print('进入runstep')
        if self.run_step_fg:
            if not self.t: #初次执行
                print(self.g, self.pre_sheet)
                self.t = Predict_Analyse(self.g, self.pre_sheet)
                print('Start')
                # text  = self.example.toPlainText()
                self.t.run(self.text)
                print('执行runstep')
            if self.t.step_fg:
                stack, input, info = self.t.doPreAnly_by_step()
                if self.idx % 2 == 0:
                    qb = QBrush(QColor(100, 149, 237))
                else:
                    qb = QBrush(QColor(176, 196, 222))
                item = QTableWidgetItem(str(self.idx+1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(qb)
                self.proeeed.setItem(self.idx, 0, item)
                item = QTableWidgetItem(stack)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(qb)
                self.proeeed.setItem(self.idx, 1, item)
                item = QTableWidgetItem(input)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(qb)
                self.proeeed.setItem(self.idx, 2, item)
                item = QTableWidgetItem(info)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(qb)
                self.proeeed.setItem(self.idx, 3, item)
                self.idx += 1
                self.proeeed.update()
                if info in ['匹配失败', '匹配成功']:
                    # 暂时关闭此功能
                    self.run_step_fg = False
                    self.t = None
                    self.idx = 0
                print('执行runstep完毕')
                print(stack,':::', input)
            else:
                print('匹配完毕')
                self.t = None
