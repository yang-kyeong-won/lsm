import sys
import pandas as pd
import ntpath

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

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
            rows.setText(str(widget.rowCount()-1))              # 첫 행은 제외
            columns.setText(str(widget.columnCount()))
        else:
            print("파일 안 골랐음")

    # TableWidget 구성 함수
    def create_table_widget(self, widget, df):
        widget.setRowCount(len(df.index)+1)                     # 첫 행에 Combobox 넣기 위해 행 갯수 1 늘림
        widget.setColumnCount(len(df.columns))
        # widget.setHorizontalHeaderLabels(df.columns)
        # widget.setVerticalHeaderLabels(df.index)
        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index+1, col_index, item)    # 첫 행 비워 놓고 데이터 채우기
        colcount = widget.columnCount()
        for i in range(0, colcount):
            locals()['cb{}'.format(i)] = QComboBox(self)    # 콤보박스 동적할당
            cb = locals()['cb{}'.format(i)]
            cb.addItem("문자열")
            cb.addItem("금액/수량/비율")
            cb.addItem("여부 > Y, N")
            cb.addItem("여부지정")
            cb.addItem("날짜지정")
            cb.addItem("전화번호")
            cb.addItem("우편번호")
            cb.addItem("사업자번호")
            widget.setCellWidget(0, i, cb)

    # 진단 버튼 클릭 함수
    def pushBt_diagnosis_clicked(self, state, widget):
        # 열 개수 추출
        col_count = widget.columnCount()
        row_count = widget.rowCount()

        for i in range(0, col_count):            # 열 데이터 형태, 항목명 점검
            # 열 이름 하나씩 추출
            data = widget.item(1, i)
            cBox = widget.cellWidget(0, i).currentText()
            if data.text().encode().isalpha():
                data.setBackground(QtGui.QColor(255, 0, 0))

            for j in range(2, row_count):
                row_data = widget.item(j, i)
                if row_data.text() == "-" or row_data.text() == " ":    # 모든 열에서 "-", " " 값 비허용
                    row_data.setBackground(QtGui.QColor(255, 0, 0))
                if not row_data.text() == "":   # 모든 열에서 공백 허용
                    continue
                if cBox == "문자열":   # "문자열" 규칙 모든 값 허용
                    continue
                elif cBox == "금액/수량/비율":    # "금액/수량/비율" 규칙 숫자 아닌 값 비허용
                    if not row_data.text().isdigit():
                        row_data.setBackground(QtGui.QColor(255, 0, 0))
                elif cBox == "여부 > Y, N":     # "여부 > Y, N" 규칙 "Y", "N" 아닌 값 비허용
                    print("여부")
                    if not row_data.text() == "Y" or row_data.text() == "N":
                        row_data.setBackground(QtGui.QColor(255, 0, 0))


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
