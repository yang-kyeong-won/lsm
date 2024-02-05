import sys
import pandas as pd
import ntpath
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('initial_screen.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 파일선택 버튼 클릭
        self.pushBt_file_chc.clicked.connect(lambda state,
                                                    widget=self.tableWidget,
                                                    announce=self.nochcFile_announce,
                                                    fileName=self.txtBr_file_nm,
                                                    rows=self.rows_count,
                                                    columns=self.columns_count: self.pushBt_file_chc_clicked(state,
                                                                                                            widget,
                                                                                                            announce,
                                                                                                            fileName,
                                                                                                            rows,
                                                                                                            columns))
        # 진단 버튼 클릭
        self.pushBt_diagnosis.clicked.connect(
            lambda state, widget=self.tableWidget: self.pushBt_diagnosis_clicked(state, widget))

        self.pushBt_restart.clicked.connect(lambda state,
                                                    widget=self.tableWidget,
                                                    announce=self.nochcFile_announce,
                                                    fileName=self.txtBr_file_nm,
                                                    rows=self.rows_count,
                                                    columns=self.columns_count: self.pushBt_restart_clicked(state,
                                                                                                             widget,
                                                                                                             announce,
                                                                                                             fileName,
                                                                                                             rows,
                                                                                                             columns))

    # 파일선택 버튼 클릭 함수
    def pushBt_file_chc_clicked(self, state, widget, announce, fileName, rows, columns):
        # 파일 경로 추출
        fname = QFileDialog.getOpenFileName(self, '파일 열기', '', 'All File(*)', 'All Files(*.*)')
        if fname[0]:
            # 파일 읽어서 Dataframe 채우기
            df = pd.read_csv(fname[0], encoding='cp949', header=None)
            # 파일 이름 추출 및 파일명 출력
            fileName.setText(ntpath.basename(fname[0]))
            # Table widget 알림말 제거
            announce.clear()
            # Table widget 구성
            self.create_table_widget(widget, df)
            # 행, 열 갯수 출력
            rows.setText(str(widget.rowCount()))
            columns.setText(str(widget.columnCount()))
        else:
            print("파일 안 골랐음")

    # TableWidget 구성 함수
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

    # 진단 버튼 클릭 함수
    def pushBt_diagnosis_clicked(self, state, widget):
        # 열 이름 체크
        isalpha = 0
        # 열 개수 추출
        colcount = widget.columnCount()
        for i in range(0, colcount):
            # 열 이름 하나씩 추출
            data = widget.item(0, i).text()
            if data.encode().isalpha():
                # 열 이름 영어 -> isalpha 1 증가
                isalpha = isalpha + 1
            else:
                continue
        if isalpha == colcount:
            print("열 이름 모두 영어")
        else:
            print("열 이름 한글 존재")

    # 재시작 버튼 클릭 함수
    def pushBt_restart_clicked(self, state, widget, announce, fileName, rows, columns):
        widget.clear()
        widget.setRowCount(0)
        widget.setColumnCount(0)
        announce.setText("선택된 csv 파일이 없습니다.")
        fileName.clear()
        rows.clear()
        columns.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
