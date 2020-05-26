import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from MainUI import  Ui_MainWindow
from VocaWindow import  Ui_self
from attribute_sheet_window import Ui_AttributeWindow
from predictive_parsing_window import Ui_MyPreAnalyseWindow
from dga_window import My_DGA_window
from AutoMata_Ui import Auto_Mata
from Op_First_Ui import Op_First
# from opfirst_window import My_Op_window

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    Ui = Ui_MainWindow()
    # Ui = Ui_MyPreAnalyseWindow()
    Ui.setupUi(mainwindow)

    qw = Ui_self()
    Ui.Voca.triggered.connect(qw.insert_data)

    sw1 = Ui_AttributeWindow()
    Ui.Midwaycode.triggered.connect(sw1.insert_data_m)
    sw2 = Ui_AttributeWindow()

    # 预测分析界面
    pre_analyse_widget = QWidget()
    pre_analyse_window = Ui_MyPreAnalyseWindow()
    pre_analyse_window.setupUi(pre_analyse_widget)
    Ui.LL_1.triggered.connect(pre_analyse_widget.show)

    # 算符优先分析界面
    op_first_widget = QWidget()
    op_first_window = Op_First()
    op_first_window.setupUi(op_first_widget)
    Ui.Opfirst.triggered.connect(op_first_widget.show)


    # DGA优化界面
    dga_widget = QWidget()
    dga_window = My_DGA_window()
    dga_window.setupUi(dga_widget)
    Ui.DGA.triggered.connect(dga_widget.show)

    # 自动机界面
    auto_mata_widget = QWidget()
    auto_mata_window = Auto_Mata()
    auto_mata_window.setupUi(auto_mata_widget)
    Ui.NFA_DFA_MFA.triggered.connect(auto_mata_widget.show)

    mainwindow.show()
    sys.exit(app.exec_())

