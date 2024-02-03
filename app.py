import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('initial_screen.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushBt_file_chc.clicked.connect(self.pushBt_file_chc_clicked)
        self.pushBt_diagnosis.clicked.connect(self.pushBt_diagnosis_clicked)

    def pushBt_file_chc_clicked(self):
        fname = QFileDialog.getOpenFileName(self, '파일 열기', '', 'All File(*)', 'All Files(*.*)')
        if fname[0]:
            print("파일 경로 : " + fname[0])
            global df
            df = pd.read_csv(fname[0], encoding='cp949')
            print(df)
        else:
            print("파일 안 골랐음")
    def pushBt_diagnosis_clicked(self):
        # 열 이름 체크
        isalpha = 0
        for i in df.columns:
            if i.encode().isalpha():
                isalpha = isalpha + 1
            else:
                continue
        if isalpha == len(df.columns):
            print("열 이름 모두 영어")
        else:
            print("열 이름 한글 존재")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()