# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opfirst.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from operator_first import *

class Op_First(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 700)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.grammar = QtWidgets.QTextEdit(self.groupBox)
        self.grammar.setObjectName("grammar")
        self.verticalLayout_3.addWidget(self.grammar)
        self.button_Confirm = QtWidgets.QPushButton(self.groupBox)
        self.button_Confirm.setObjectName("button_Confirm")
        self.verticalLayout_3.addWidget(self.button_Confirm)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_3.addWidget(self.textBrowser_2)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sheet = QtWidgets.QTableWidget(self.groupBox_4)
        self.sheet.setObjectName("sheet")
        self.sheet.setColumnCount(0)
        self.sheet.setRowCount(0)
        self.verticalLayout.addWidget(self.sheet)
        self.verticalLayout_8.addWidget(self.groupBox_4)
        self.groupBox_6 = QtWidgets.QGroupBox(Form)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.example = QtWidgets.QTextEdit(self.groupBox_6)
        self.example.setObjectName("example")
        self.verticalLayout_6.addWidget(self.example)
        self.button_Parse = QtWidgets.QPushButton(self.groupBox_6)
        self.button_Parse.setObjectName("button_Parse")
        self.verticalLayout_6.addWidget(self.button_Parse)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_8.addWidget(self.groupBox_6)
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.step = QtWidgets.QTableWidget(self.groupBox_5)
        self.step.setObjectName("step")
        self.step.setColumnCount(0)
        self.step.setRowCount(0)
        self.verticalLayout_2.addWidget(self.step)
        self.verticalLayout_8.addWidget(self.groupBox_5)
        self.verticalLayout_8.setStretch(0, 5)
        self.verticalLayout_8.setStretch(1, 2)
        self.verticalLayout_8.setStretch(2, 5)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(2, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.button_Confirm.clicked.connect(lambda: self.judge_grammar())


    def judge_grammar(self):
        g = self.grammar.toPlainText()
        isflag, firstvt, lastvt, table, state = '', '', '', '', ''
        try:
            opf = Oper_First(grammer=g)
            isflag, firstvt, lastvt, table, state = opf.judge_grammar()
        except:
            isflag = False
        print(isflag)

        if not isflag:
            self.button_Parse.setEnabled(False)
        else:
            f_t, l_t, t_t = '', '', ''
            for key, value in firstvt.items():
                f_t += "FIRSTVT(%s) = {%s}\n" % (key, str(value)[1:-1])
            print(f_t)
            self.textBrowser.setText(f_t)
            for key, value in lastvt.items():
                l_t += "LASTVT(%s) = {%s}\n" % (key, str(value)[1:-1])
            print(l_t)
            self.textBrowser_2.setText(l_t)

            print(state)
            self.sheet.setRowCount(len(state))
            self.sheet.setColumnCount(len(state))
            self.sheet.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.sheet.resizeColumnToContents(0)

            self.sheet.setHorizontalHeaderLabels(state)
            self.sheet.setVerticalHeaderLabels(state)

            for i in range(len(state)):
                for j in range(len(state)):
                    v = table[i][j]
                    item = QTableWidgetItem(v)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    if i % 2 == 0:
                        item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                    else:
                        item.setBackground(QBrush(QColor(176, 196, 222)))
                    self.sheet.setItem(i, j, item)


            self.button_Parse.setEnabled(True)
            input = self.example.toPlainText()
            self.button_Parse.clicked.connect(lambda : self.run_op_first(g, input))


    def run_op_first(self, grammar, input=""):
        opf = Oper_First(grammer=grammar, input_str=input)
        steps = opf.run()
        # print(steps)

        self.step.setRowCount(len(steps)-1)
        self.step.setColumnCount(len(steps[0]))
        self.step.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.step.resizeColumnToContents(0)

        self.step.setHorizontalHeaderLabels(steps[0])
        self.step.verticalHeader().setVisible(False)
        # self.step.setVerticalHeaderLabels(steps[0])

        for i in range(1,len(steps)):
            for j in range(len(steps[0])):
                v = steps[i][j]
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i % 2 == 0:
                    item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                else:
                    item.setBackground(QBrush(QColor(176, 196, 222)))
                self.step.setItem(i-1, j, item)







    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OP_first"))
        self.groupBox.setTitle(_translate("Form", "OP_first_grammar"))
        self.grammar.setText("E->E+T\nE->T\nT->T*F\nT->F\nF->P|F\nF->P\nP->(E)\nP->i")
        self.button_Confirm.setText(_translate("Form", "Confirm"))
        self.groupBox_2.setTitle(_translate("Form", "First_VT"))
        self.groupBox_3.setTitle(_translate("Form", "Last_VT"))
        self.groupBox_4.setTitle(_translate("Form", "Sheet"))
        self.groupBox_6.setTitle(_translate("Form", "Example"))
        self.button_Parse.setText(_translate("Form", "Parse"))
        self.groupBox_5.setTitle(_translate("Form", "Step"))
