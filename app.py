import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

form_class = uic.loadUiType('initial_screen.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushBt_file_chc.clicked.connect(self.pushBt_file_chc_clicked)

    def pushBt_file_chc_clicked(self):
        fname = QFileDialog.getOpenFileName(self, '파일 열기', '', 'All File(*)', 'All Files(*.*)')
        if fname[0]:
            print("파일 선택됨 파일 경로는 아래와 같음")
            print(fname[0])
        else:
            print("파일 안 골랐음")
        df = pd.read_csv(fname[0])
        print(df)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()