import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('initial_screen.ui')[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushBt_file_chc.clicked.connect(lambda state, widget = self.tableWidget: self.pushBt_file_chc_clicked(state, widget))
        self.pushBt_diagnosis.clicked.connect(lambda state, widget = self.tableWidget: self.pushBt_diagnosis_clicked(state, widget))

    def pushBt_file_chc_clicked(self, state, widget):
        fname = QFileDialog.getOpenFileName(self, '파일 열기', '', 'All File(*)', 'All Files(*.*)')
        if fname[0]:
            print("파일 경로 : " + fname[0])
            df = pd.read_csv(fname[0], encoding='cp949', header=None)
            print(df)
            self.create_table_widget(widget, df)
        else:
            print("파일 안 골랐음")

    def create_table_widget(self, widget, df):
        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        # widget.setHorizontalHeaderLabels(df.columns)
        # widget.setVerticalHeaderLabels(df.index)

        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)

    def pushBt_diagnosis_clicked(self, state, widget):
        # 열 이름 체크
        isalpha = 0
        colcount = widget.columnCount()
        print(colcount)
        for i in range(0, colcount):
            data = widget.item(0, i).text()
            print(data)
            if data.encode().isalpha():
                isalpha = isalpha + 1
            else:
                continue
        if isalpha == colcount:
            print("열 이름 모두 영어")
        else:
            print("열 이름 한글 존재")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
