# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'New.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# from voca import Ui_VacoWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from extract_word import parseString
from assembly_instruction import gen_assemcodes
# from PyQt5.Qsci import *
import  sys
import  os
import  pickle
import  threading
import chardet
from LR1_grammar import LR1_G
# from testLR1_const import doLR1
from translate import Translate

# 加载语言包


with open('configs/OP.dll', 'r',encoding = 'utf-8') as f:
    lang_file = f.read()


def load_lang(file):
    with open(file, 'r', encoding = 'utf-8') as f:
        Language = f.read().split('\n')
    return Language

def check_code(text):
    adchar = chardet.detect(text)
    # 由于windows系统的编码有可能是Windows-1254,打印出来后还是乱码,所以不直接用adchar['encoding']编码
    #if adchar['encoding'] is not None:
    #    true_text = text.decode(adchar['encoding'], "ignore")
    if adchar['encoding'] == 'gbk' or adchar['encoding'] == 'GBK' or adchar['encoding'] == 'GB2312':
        true_text = text.decode('GB2312', "ignore")
    elif adchar['encoding'] in ['ISO-8859-1', 'TIS-620', 'EUC-JP']:
        true_text = text.decode('ansi', "ignore")
    else:
        true_text = text.decode('utf-8', "ignore")
    return true_text


Language = load_lang(lang_file)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1140, 909)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setMaximumWidth(2)
        # MainWindow.setCentralWidget(self.centralwidget)  # 屏蔽中心面板

        # 加载本地历史记录

        try:
            self.history_filename = pickle.load(open('data/history.pkl', 'rb'))
        except:
            self.history_filename = []

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1140, 26))
        self.menubar.setObjectName("menubar")
        self.File = QtWidgets.QMenu(self.menubar)
        self.File.setObjectName("File")
        self.menu = QtWidgets.QMenu(self.File)
        self.menu.setObjectName("menu")
        self.Edit = QtWidgets.QMenu(self.menubar)
        self.Edit.setObjectName("Edit")
        self.Format = QtWidgets.QMenu(self.menubar)
        self.Format.setObjectName("Format")
        self.Build = QtWidgets.QMenu(self.menubar)
        self.Build.setObjectName("Build")
        self.View = QtWidgets.QMenu(self.menubar)
        self.View.setObjectName("View")
        self.Help = QtWidgets.QMenu(self.menubar)
        self.Help.setObjectName("Help")
        self.Language = QtWidgets.QMenu(self.menubar)
        self.Language.setObjectName("Language")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_Edit = QtWidgets.QDockWidget(MainWindow)

        self.dockWidget_Edit.setObjectName("dockWidget_Edit")

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.dockWidget_Edit.setWidget(self.textEdit)
        MainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWidget_Edit)

        self.dockWidget_Menu = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_Menu.setObjectName("dockWidget_Menu")

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.dockWidget_Menu.setWidget(QtWidgets.QTreeWidget())
        self.dockWidget_Menu.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget_Menu.setFloating(False)
        self.dockWidget_Menu.setMaximumWidth(300)
        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_Menu)

        self.row_col = QtWidgets.QDockWidget(MainWindow)
        self.row_col.setObjectName("row_col")
        MainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.row_col)

        self.dockWidget_Info = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_Info.setObjectName("dockWidget_Info")
        # self.dockWidget_Info.setMaximumHeight(300)
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setObjectName("textBrowser")
        self.dockWidget_Info.setWidget(self.textBrowser)
        MainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWidget_Info)


        self.New = QtWidgets.QAction(MainWindow)
        self.New.setCheckable(False)
        self.New.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/新建文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.New.setIcon(icon)
        self.New.setObjectName("New")
        self.Open = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/打开文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Open.setIcon(icon1)
        self.Open.setObjectName("Open")
        self.Save = QtWidgets.QAction(MainWindow)
        self.Save.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/保存.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Save.setIcon(icon2)
        self.Save.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.Save.setObjectName("Save")
        self.SaveAs = QtWidgets.QAction(MainWindow)
        self.SaveAs.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/导出 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveAs.setIcon(icon3)
        self.SaveAs.setObjectName("SaveAs")
        self.Exit = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Exit.setIcon(icon4)
        self.Exit.setObjectName("Exit")

        self.Undo = QtWidgets.QAction(MainWindow)
        self.Undo.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/撤销.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Undo.setIcon(icon5)
        self.Undo.setObjectName("Undo")
        self.Redo = QtWidgets.QAction(MainWindow)
        self.Redo.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/反撤销.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Redo.setIcon(icon6)
        self.Redo.setObjectName("Redo")
        self.Cut = QtWidgets.QAction(MainWindow)
        self.Cut.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/剪切.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Cut.setIcon(icon7)
        self.Cut.setObjectName("Cut")
        self.Copy = QtWidgets.QAction(MainWindow)
        self.Copy.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/复制.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Copy.setIcon(icon8)
        self.Copy.setObjectName("Copy")
        self.Paste = QtWidgets.QAction(MainWindow)
        self.Paste.setObjectName("Paste")
        self.Delete = QtWidgets.QAction(MainWindow)
        self.Delete.setEnabled(True)
        self.Delete.setObjectName("Delete")
        self.Find = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/查找.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Find.setIcon(icon9)
        self.Find.setObjectName("Find")
        self.Replace = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/替换.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Replace.setIcon(icon10)
        self.Replace.setObjectName("Replace")
        self.All = QtWidgets.QAction(MainWindow)
        self.All.setObjectName("All")
        self.Font = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/字体设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Font.setIcon(icon11)
        self.Font.setObjectName("Font")
        self.Color = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("icons/颜色.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Color.setIcon(icon12)
        self.Color.setObjectName("Color")
        self.List = QtWidgets.QAction(MainWindow)
        self.List.setCheckable(True)
        self.List.setObjectName("List")
        self.EditView = QtWidgets.QAction(MainWindow)
        self.EditView.setCheckable(True)
        self.EditView.setObjectName("EditView")
        self.Info = QtWidgets.QAction(MainWindow)
        self.Info.setCheckable(True)
        self.Info.setObjectName("Info")
        self.Voca = QtWidgets.QAction(MainWindow)
        self.Voca.setEnabled(False)
        self.Voca.setObjectName("Voca")
        self.NFA_DFA_MFA = QtWidgets.QAction(MainWindow)
        # self.NFA_DFA_MFA.setEnabled(False)
        self.NFA_DFA_MFA.setObjectName("NFA_DFA_MFA")
        self.Grammar = QtWidgets.QAction(MainWindow)
        self.Grammar.setEnabled(False)
        self.Grammar.setObjectName("Grammar")
        self.LL_1 = QtWidgets.QAction(MainWindow)
        self.LL_1.setEnabled(True)
        self.LL_1.setObjectName("LL_1")
        self.Opfirst = QtWidgets.QAction(MainWindow)
        self.Opfirst.setObjectName("Opfirst")
        self.DGA = QtWidgets.QAction(MainWindow)
        self.DGA.setObjectName("LR")
        self.Midwaycode = QtWidgets.QAction(MainWindow)
        self.Midwaycode.setObjectName("Midwaycode")
        self.Midwaycode.setEnabled(False)
        self.Targetcode = QtWidgets.QAction(MainWindow)
        self.Targetcode.setObjectName("Targetcode")
        self.Targetcode.setEnabled(False)
        self.chinese = QtWidgets.QAction(MainWindow)
        self.chinese.setCheckable(True)
        self.chinese.setObjectName("chinese")
        self.English = QtWidgets.QAction(MainWindow)
        self.English.setCheckable(True)
        self.English.setObjectName("English")
        self.Help_YSL = QtWidgets.QAction(MainWindow)
        self.Help_YSL.setObjectName("Help_YSL")
        self.About = QtWidgets.QAction(MainWindow)
        self.About.setObjectName("About")

        self.File.addAction(self.New)
        self.File.addAction(self.Open)
        self.File.addAction(self.menu.menuAction())
        self.File.addSeparator()
        self.File.addAction(self.Save)
        self.File.addAction(self.SaveAs)
        self.File.addSeparator()
        self.File.addAction(self.Exit)
        self.Edit.addAction(self.Undo)
        self.Edit.addAction(self.Redo)
        self.Edit.addSeparator()
        self.Edit.addAction(self.Cut)
        self.Edit.addAction(self.Copy)
        self.Edit.addAction(self.Paste)
        self.Edit.addAction(self.Delete)
        self.Edit.addSeparator()
        self.Edit.addAction(self.Find)
        self.Edit.addAction(self.Replace)
        self.Edit.addAction(self.All)
        self.Format.addAction(self.Font)
        self.Format.addAction(self.Color)
        self.Build.addAction(self.Voca)
        self.Build.addAction(self.NFA_DFA_MFA)
        self.Build.addSeparator()
        self.Build.addAction(self.Grammar)
        self.Build.addAction(self.LL_1)
        self.Build.addAction(self.Opfirst)
        self.Build.addAction(self.DGA)
        self.Build.addSeparator()
        self.Build.addAction(self.Midwaycode)
        self.Build.addSeparator()
        self.Build.addAction(self.Targetcode)
        self.View.addAction(self.List)
        self.View.addAction(self.EditView)
        self.View.addAction(self.Info)
        self.Help.addAction(self.Help_YSL)
        self.Help.addAction(self.About)
        self.Language.addAction(self.chinese)
        self.Language.addAction(self.English)
        self.menubar.addAction(self.File.menuAction())
        self.menubar.addAction(self.Edit.menuAction())
        self.menubar.addAction(self.Format.menuAction())
        self.menubar.addAction(self.Build.menuAction())
        self.menubar.addAction(self.View.menuAction())
        self.menubar.addAction(self.Language.menuAction())
        self.menubar.addAction(self.Help.menuAction())
        self.tree = QtWidgets.QTreeWidget()

        self.List.setChecked(True)
        self.EditView.setChecked(True)
        self.Info.setChecked(True)
        self.finished = False
        self.history_path = os.getcwd()
        self.setTree()
        self.addRecent(MainWindow)
        self.retranslateUi(MainWindow)
        self.textEdit.setEnabled(False)



        pa = self.textEdit.palette();
        pa.setColor(QPalette.Base, QColor(220, 220, 220))
        self.textEdit.setPalette(pa)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def addRecent(self, MainWindow):
        self.rfile = []
        for i,f in enumerate(self.history_filename[:5]):
            qa = QtWidgets.QAction(MainWindow)
            qa.setObjectName("rfile{}".format(i))
            self.rfile.append(qa)
            self.menu.addAction(qa)

    def printRfile(self):
        _translate = QtCore.QCoreApplication.translate
        for i,f in enumerate(self.history_filename):
            self.rfile[i].setText(_translate("MainWindow", f))




    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Sample Compiler"))
            self.File.setTitle(_translate("MainWindow", Language[0]))
            self.menu.setTitle(_translate("MainWindow", Language[1]))
            self.Edit.setTitle(_translate("MainWindow", Language[2]))
            self.Format.setTitle(_translate("MainWindow", Language[3]))
            self.Build.setTitle(_translate("MainWindow", Language[4]))
            self.View.setTitle(_translate("MainWindow", Language[5]))
            self.Help.setTitle(_translate("MainWindow", Language[6]))
            self.Language.setTitle(_translate("MainWindow", Language[7]))
            self.dockWidget_Edit.setWindowTitle(_translate("MainWindow", Language[8]))
            self.dockWidget_Menu.setWindowTitle(_translate("MainWindow", Language[9]))
            self.dockWidget_Info.setWindowTitle(_translate("MainWindow", Language[10]))
            self.row_col.setWindowTitle(_translate("MainWindow", Language[11]))
            self.New.setText(_translate("MainWindow", Language[12]))
            self.New.setShortcut(_translate("MainWindow", "Ctrl+Alt+Ins"))
            self.Open.setText(_translate("MainWindow", Language[13]))
            self.Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
            self.Save.setText(_translate("MainWindow", Language[14]))
            self.Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
            self.SaveAs.setText(_translate("MainWindow", Language[15]))
            self.SaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
            self.Exit.setText(_translate("MainWindow", Language[16]))
            self.Exit.setShortcut(_translate("MainWindow", "Esc"))
            # self.action_4.setText(_translate("MainWindow", Language[17]))
            # ？？？？
            self.printRfile()
            self.Undo.setText(_translate("MainWindow", Language[18]))
            self.Undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
            self.Redo.setText(_translate("MainWindow", Language[19]))
            self.Redo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
            self.Cut.setText(_translate("MainWindow", Language[20]))
            self.Cut.setShortcut(_translate("MainWindow", "Ctrl+X"))
            self.Copy.setText(_translate("MainWindow", Language[21]))
            self.Copy.setShortcut(_translate("MainWindow", "Ctrl+C"))
            self.Paste.setText(_translate("MainWindow", Language[22]))
            self.Paste.setShortcut(_translate("MainWindow", "Ctrl+V"))
            self.Delete.setText(_translate("MainWindow", Language[23]))
            self.Delete.setShortcut(_translate("MainWindow", "Del"))
            self.Find.setText(_translate("MainWindow", Language[24]))
            self.Find.setShortcut(_translate("MainWindow", "Ctrl+F"))
            self.Replace.setText(_translate("MainWindow", Language[25]))
            self.Replace.setShortcut(_translate("MainWindow", "Ctrl+T"))
            self.All.setText(_translate("MainWindow", Language[26]))
            self.Font.setText(_translate("MainWindow", Language[27]))
            self.Color.setText(_translate("MainWindow", Language[28]))
            self.List.setText(_translate("MainWindow", Language[29]))
            self.EditView.setText(_translate("MainWindow", Language[30]))
            self.Info.setText(_translate("MainWindow", Language[31]))
            self.Voca.setText(_translate("MainWindow", Language[32]))
            self.Voca.setShortcut(_translate("MainWindow", "Ctrl+Alt+C"))
            self.NFA_DFA_MFA.setText(_translate("MainWindow", Language[33]))
            self.Grammar.setText(_translate("MainWindow", Language[34]))
            self.LL_1.setText(_translate("MainWindow", Language[35]))
            self.Opfirst.setText(_translate("MainWindow", Language[36]))
            self.DGA.setText(_translate("MainWindow", Language[37]))
            self.Midwaycode.setText(_translate("MainWindow", Language[38]))
            self.Targetcode.setText(_translate("MainWindow", Language[39]))
            self.chinese.setText(_translate("MainWindow", Language[40]))
            self.English.setText(_translate("MainWindow", Language[41]))
            self.Help_YSL.setText(_translate("MainWindow", Language[42]))
            self.About.setText(_translate("MainWindow", Language[43]))

            print(lang_file)
            if lang_file == 'configs/zh.txt':
                self.chinese.setChecked(True)
            else:
                self.English.setChecked(True)

            # 添加绑定事件
            self.addTrigged()


    def addTrigged(self):
        self.Open.triggered.connect(self.openFile)
        self.About.triggered.connect(self.about)
        self.SaveAs.triggered.connect(self.saveAsFile)
        self.Exit.triggered.connect(self.exit)
        self.Help_YSL.triggered.connect(self.help)
        self.Copy.triggered.connect(self.copy)
        self.Cut.triggered.connect(self.cut)
        self.Paste.triggered.connect(self.paste)
        self.Undo.triggered.connect(self.undo)
        self.Find.triggered.connect(self.find)
        self.textEdit.cursorPositionChanged.connect(self.showColandRow)
        self.List.triggered.connect(self.viewList)
        self.EditView.triggered.connect(self.viewEdit)
        self.Info.triggered.connect(self.viewInfo)
        self.Voca.triggered.connect(self.voca)
        self.Font.triggered.connect(self.font)
        self.Color.triggered.connect(self.color)
        self.tree.doubleClicked.connect(self.treeClicked)
        self.tree.clicked.connect(self.Clicked)
        self.chinese.triggered.connect(self.setZHLang)
        self.English.triggered.connect(self.setENLang)
        self.New.triggered.connect(self.new)
        self.Save.triggered.connect(self.save)
        self.All.triggered.connect(self.select_all)
        self.Opfirst.triggered.connect(self.opfrist)
        self.Midwaycode.triggered.connect(self.midcode)

        for f in self.rfile:
            f.triggered.connect(self.openRfile)

        self.Grammar.triggered.connect(self.doGrammer)
        self.LL_1.triggered.connect(self.left1)
        self.Targetcode.triggered.connect(self.targetcode)

    def targetcode(self):
        '''
        生成汇编代码
        :return:
        '''
        self.textBrowser.clear()
        t = Translate()
        s = self.textEdit.toPlainText()
        fg, info = t.entry(s)
        if fg:
            # t.optimize_code()
            ass_codes = gen_assemcodes(t.codes)
            info = ''.join(ass_codes)
            self.textBrowser.setText(info)
            self.textBrowser.selectAll()
            self.textBrowser.copy()
            # 提示已经复制到剪切板
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'Tips',
                                '汇编代码已复制!')
        else:
            pickle.dump((False, None), open('data/midway_sheet.pkl', 'wb'))
            info = '----- error !\n' + '\n'.join(info)
            self.textBrowser.setText(info)
        self.save()

    def left1(self):
        print('LL1 预测分析')


    def midcode(self):
        '''
        生成中间代码
        :return:
        '''
        self.textBrowser.clear()
        t = Translate()
        s = self.textEdit.toPlainText()
        fg, info = t.entry(s)
        if fg:
            t.optimize_code()
            pickle.dump((True, t.codes), open('data/midway_sheet.pkl', 'wb'))
        else:
            pickle.dump((False, None), open('data/midway_sheet.pkl', 'wb'))
            info = '----- error !\n' + '\n'.join(info)
            self.textBrowser.setText(info)
        self.save()



    def opfrist(self):
        '''
        生成属性列表
        :return:
        '''
        s = self.textEdit.toPlainText()
        print('yyyyyyy')
        # doLR1(s)
    def doGrammer(self):

        # 清理信息栏的文字
        self.textBrowser.clear()

        texts = self.textEdit.toPlainText()
        print(texts)
        anlyse = LR1_G()
        fg, errors = anlyse.entry(texts)

        if fg:
            info = '匹配成功， 未发现错误！'
        else:
            info = '\n\t'.join(errors)
            info = '\n\t'+info
        self.textBrowser.setText(info)
        self.save()
        self.tree.update()



    def saveHistory(self):
        pickle.dump(self.history_filename, open('data/history.pkl', 'wb'))

    def openRfile(self):

        self.initControl()
        sender = self.menu.sender()

        filename = sender.text()
        try:
            with open(filename, 'rb') as f:
                text = f.read()
                text = check_code(text)
            self.updata_text_window(filename)
            self.textEdit.setText(text)
            self.filename = filename
        except FileNotFoundError:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'Tips',
                                'No Such File!')


    def Clicked(self):
        pass

    def new(self):

        # 清空textEdit

        self.textEdit.setEnabled(True)
        self.textEdit.clear()
        self.initControl()
        path = os.getcwd()
        list_files = os.listdir()
        filename_base = 'Untitled'
        for i in range(100):
            self.filename = filename_base + str(i)+'.txt'
            if self.filename not in list_files:
                break

        with open(self.filename, 'w', encoding = 'utf-8') as f:
            f.write('')
        self.updata_text_window(self.filename)
        self.Save.setEnabled(True)
        self.SaveAs.setEnabled(True)

    def updata_text_window(self, text):
        _translate = QtCore.QCoreApplication.translate
        self.dockWidget_Edit.setWindowTitle(_translate("MainWindow", text + '\t [Text Edit]'))



    def setZHLang(self):
        if self.chinese.isChecked():
            with open('configs/OP.dll', 'w', encoding = 'utf-8') as f:
                f.write('configs/zh.txt')

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'YSL_compier',
                              '重启软件生效!')
            self.English.setChecked(False)

    def setENLang(self):
        if self.English.isChecked():
            with open('configs/OP.dll', 'w', encoding = 'utf-8') as f:
                f.write('configs/en.txt')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            qw = QtWidgets.QWidget()
            qw.setWindowIcon(icon)
            QMessageBox.warning(qw, 'YSL_compier',
                                'Restart to take effect!')
            self.chinese.setChecked(False)

    def setTree(self):

        self.tree.clear()
        # 定义一些常用的icon
        icon_folder = QtGui.QIcon()
        icon_folder.addPixmap(QtGui.QPixmap("icons/文件夹.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.tree.setColumnCount(1)
        self.tree.setColumnWidth(0, 50)
        self.tree.setHeaderLabels(["EXPLORER"])
        # self.tree.setIconSize(QtGui.QSiz(25, 25))
        # self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # 获取当前目录
        dirs = os.listdir(self.history_path)
        path = self.history_path

        root = QtWidgets.QTreeWidgetItem(self.tree)
        root.setText(0, path)
        root.setIcon(0, icon_folder)

        self.creatTree(dirs, root, path)
        self.dockWidget_Menu.setWidget(self.tree)

    def creatTree(self, dirs, root, path):
        '''
        创建文件管理导航
        :return:
        '''
        icon_folder = QtGui.QIcon()
        icon_folder.addPixmap(QtGui.QPixmap("icons/文件夹.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_file = QtGui.QIcon()
        icon_file.addPixmap(QtGui.QPixmap("icons/文本.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        for i in dirs:
            path_new = path + '\\' + i
            if os.path.isdir(path_new):

                child = QtWidgets.QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, icon_folder)
                dirs_new = os.listdir(path_new)
                self.creatTree(dirs_new, child, path_new)
            else:
                if i.split('.')[-1].lower() in ['txt','c','py']:
                    child = QtWidgets.QTreeWidgetItem(root)
                    child.setText(0, i)
                    child.setIcon(0, icon_file)

    def treeClicked(self, e):

        print('pppyyy')
        self.initControl()
        self.tree.update()
        item = self.tree.currentItem()
        fpath = item.text(0)
        try:
            temp = item
            while temp.parent() is not None:
                fpath = temp.parent().text(0)+'\\'+ fpath
                temp = temp.parent()
        except:
            print('获取文件路径失败！')

        if os.path.isfile(fpath):
            #打开文本

            with open(fpath, 'rb') as f:
                text = f.read()
                text = check_code(text)
                self.textEdit.setText(text)
                # 更新编辑区标题
                self.updata_text_window(fpath)
        # 设置当前文件为界面文件， 后面用于保存
        self.filename = fpath

        self.tree.update()
        print('His', self.history_filename)
        if fpath not in self.history_filename:
            if len(self.history_filename) < 5 :
                self.history_filename = [fpath] + self.history_filename
            else:
                self.history_filename = [fpath] + self.history_filename[1:]


    def initControl(self):
        '''
        lunch some function
        :return:
        '''
        self.Save.setEnabled(True)
        self.SaveAs.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.Voca.setEnabled(True)
        self.Cut.setEnabled(True)
        self.Copy.setEnabled(True)
        self.Undo.setEnabled(True)
        self.Redo.setEnabled(True)
        self.Grammar.setEnabled(True)
        self.Targetcode.setEnabled(True)
        self.Midwaycode.setEnabled(True)


    def select_all(self):
        self.textEdit.selectAll()

    def openFile(self, q):
        '''
        调用pyqt内置的文件资源器
        :param q:
        :return:
        '''

        self.textEdit.setEnabled(True)
        qw = QtWidgets.QWidget()
        fileName1, filetype = QFileDialog.getOpenFileName(qw,
                                                          "选取文件",
                                                          self.history_path,
                                                      ";Text Files (*.txt);;C code (*.c);;Python code(*.py)")  # 设置文件扩展名过滤,注意用双分号间隔

        if not fileName1:
            return

        with open(fileName1, 'rb') as f:
            text = f.read()
            text = check_code(text)

        self.textEdit.setText(text)
        #更新编辑区标题
        self.updata_text_window(fileName1)

        self.filename = fileName1
        self.history_path = os.path.dirname(fileName1)
        self.setTree() # 刷新文件目录
        self.initControl()
        if fileName1 not in self.history_filename:
            if len(self.history_filename) < 5:
                self.history_filename = [fileName1] + self.history_filename
            else:
                self.history_filename = [fileName1] + self.history_filename[1:]


    def save(self):
        if not self.filename.startswith('Untitled'):
            with open(self.filename, 'w', encoding = 'utf-8') as f:
                f.write(self.textEdit.toPlainText())
            self.setTree()
        else:
            self.saveAsFile()
        self.saveHistory()

    def saveAsFile(self):
        '''
        保存文件
        :param q:
        :return:
        '''
        qw = QtWidgets.QWidget()
        fileName2, ok2 = QFileDialog.getSaveFileName(qw,
                                                    "文件保存",
                                                    self.history_path,
                                                    "Text Files (*.txt);;C code (*.c);;Python code(*.py)")
        text = self.textEdit.toPlainText()

        try:
            with open(fileName2, 'w', encoding = 'utf-8') as f:
                f.write(text)
                self.textBrowser.setText('>--------------------- Sucessfully! ---------------------')
            self.filename = fileName2
        except:
            self.textBrowser.setText('>--------------------- Failure! ---------------------')


        self.updata_text_window(self.filename)
        self.setTree()

    def about(self,q):
        '''
        显示帮助手册
        :param q:
        :return:
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        qw = QtWidgets.QWidget()
        qw.setWindowIcon(icon)
        reply = QMessageBox.about(qw, 'YSL_compier', 'This is my own App, Now the version is 0.0.0\n E-mail: yangeniux@gmail.com')

    def exit(self, q):
        sys.exit(0)

    def showColandRow(self):
        cursor = self.textEdit.textCursor()
        col = cursor.columnNumber() + 1
        row = cursor.blockNumber() + 1
        _translate = QtCore.QCoreApplication.translate
        self.row_col.setWindowTitle(_translate("MainWindow", "Row: "+str(row)+" Col: "+str(col)))

        if not self.Voca.isEnabled():
            self.Voca.setEnabled(True)

    def viewList(self):
        if self.List.isChecked():
            self.dockWidget_Menu.show()
        else:
            self.dockWidget_Menu.hide()

    def viewEdit(self):
        if self.EditView.isChecked():
            self.dockWidget_Edit.show()
        else:
            self.dockWidget_Edit.hide()

    def viewInfo(self):
        if self.Info.isChecked():
            self.dockWidget_Info.show()
        else:
            self.dockWidget_Info.hide()

    def copy(self, e):
        self.textEdit.copy()

    def cut(self, e):
        self.textEdit.cut()

    def paste(self, e):
        self.textEdit.paste()

    def undo(self, e):
        self.textEdit.undo()

    def find(self, e):
        #先弹窗输入要搜索的文本
        qw = QtWidgets.QWidget()
        texts = QInputDialog.getText(qw, "Find","Find Text:", QLineEdit.Normal)[0]
        if self.textEdit.find(texts, QTextDocument.FindBackward):
            ## 只能找一个
            pleatte = self.textEdit.palette()
            pleatte.setColor(QPalette.Highlight, pleatte.color(QPalette.Active, QPalette.Highlight))
            self.textEdit.setPalette(pleatte)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            QMessageBox.setWindowIcon(qw,icon)
            QMessageBox.information(qw, "Tips", "Not Found ！",QMessageBox.Ok)

    def help(self, e):
        os.startfile('configs\YSL\'s_compiler.CHM')

    def voca(self, e):

        self.save()

        #弹窗
        text = self.textEdit.toPlainText()
        res, errors = parseString(text)
        pickle.dump(res, open("vocaburary.pkl", 'wb'))

        if errors:
            error_info = ''.join([str(error) for error in errors])

            self.textBrowser.setText('Find{} Errors:\n'.format(len(errors))+error_info)
        else:
            self.textBrowser.clear()

    def font(self, e):
        self.fon, isok = QFontDialog.getFont()
        if isok:
            self.textEdit.setFont(self.fon)
            self.textEdit.update()


    def color(self, e):
        col = QColorDialog.getColor()
        if col.isValid():
            self.textEdit.setTextColor(col)
