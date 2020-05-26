# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from draw_DAG_ import draw
from create_DAG import create_DAG, optimize
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def transfer(s):
    '''
    把字符串的四元式转成list
    :param s:
    :return:
    '''
    res = []
    lines = s.split('\n')
    for line in lines:
        factors = line.split(',')
        if len(factors) == 4:  # 是四元式
            res.append((factors[0], factors[1], factors[2], factors[3]))
        else:
            return '', False
    return res, True


class My_DGA_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(795, 516)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.code = QtWidgets.QTextEdit(self.groupBox)
        self.code.setObjectName("code")
        self.verticalLayout_3.addWidget(self.code)
        self.button_Run = QtWidgets.QPushButton(self.groupBox)
        self.button_Run.setObjectName("button_Run")
        self.verticalLayout_3.addWidget(self.button_Run)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.visible = QtWidgets.QGraphicsView(self.groupBox_2)
        self.visible.setObjectName("visible")
        self.verticalLayout.addWidget(self.visible)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.opt_code = QtWidgets.QTextBrowser(self.groupBox_3)
        self.opt_code.setObjectName("opt_code")
        self.verticalLayout_2.addWidget(self.opt_code)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.code.setText('=,3.14,,T0\n*,2,T0,T1\n+,R,r,T2\n*,T1,T2,A\n=,A,,B\n*,2,T0,T3\n+,R,r,T4\n*,T3,T4,T5\n-,R,r,T6\n*,T5,T6,B')
        self.triggered()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def triggered(self):
        '''
        绑定一些事件
        :return:
        '''

        self.button_Run.clicked.connect(self.run)

    def run(self):
        s = self.code.toPlainText()
        code, fg = transfer(s)
        if fg:
            DAG = create_DAG(code)
            codes = optimize(DAG)
            info = '\n'.join([','.join(c) for c in codes])
            self.opt_code.setText(info)
            draw(DAG)
            self.visible.scene_img = QGraphicsScene()
            self.imgShow = QPixmap()
            self.imgShow.load('visible.png')
            self.imgShowItem = QGraphicsPixmapItem()
            self.imgShowItem.setPixmap(QPixmap(self.imgShow))
            # self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(self.visible.width(), self.visible.height()))  # //自己设定尺寸
            self.visible.scene_img.addItem(self.imgShowItem)
            self.visible.setScene(self.visible.scene_img)
        else:
            #弹出警告
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'Tips',
                                '代码格式错误!')
            self.opt_code.clear()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DGA"))
        self.groupBox.setTitle(_translate("Form", "Code"))
        self.button_Run.setText(_translate("Form", "Run"))
        self.groupBox_2.setTitle(_translate("Form", "Visible"))
        self.groupBox_3.setTitle(_translate("Form", "Opt_code"))
