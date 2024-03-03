import datetime
import sys
import pandas as pd
import ntpath
import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui, sip

form_class = uic.loadUiType('initial_screen.ui')[0]

df_postal = pd.read_pickle("df_postal.pkl")
print(df_postal)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.e_tableWidget.hide()   # 비교 위한 백업 테이블
        self.target = list()    # 정비 대상 리스트
        # 파일선택 버튼 클릭
        self.pushBt_file_chc.clicked.connect(lambda state,
                                                    widget=self.tableWidget,
                                                    announce=self.nochcFile_announce,
                                                    fileName=self.txtBr_file_nm,
                                                    rows=self.rows_count,
                                                    columns=self.columns_count,
                                                    e_widget=self.e_tableWidget: self.pushBt_file_chc_clicked(state,
                                                                                                            widget,
                                                                                                            announce,
                                                                                                            fileName,
                                                                                                            rows,
                                                                                                            columns,
                                                                                                            e_widget))
        # 진단 버튼 클릭
        self.pushBt_diagnosis.clicked.connect(
            lambda state, widget=self.tableWidget, e_widget=self.e_tableWidget, target = self.target: self.pushBt_diagnosis_clicked(state, widget, e_widget, target))

        self.pushBt_restart.clicked.connect(lambda state,
                                                    widget=self.tableWidget,
                                                    announce=self.nochcFile_announce,
                                                    fileName=self.txtBr_file_nm,
                                                    rows=self.rows_count,
                                                    columns=self.columns_count,
                                                    e_widget=self.e_tableWidget: self.pushBt_restart_clicked(state,
                                                                                                             widget,
                                                                                                             announce,
                                                                                                             fileName,
                                                                                                             rows,
                                                                                                             columns,
                                                                                                             e_widget))
        self.pushBt_improve.clicked.connect(
            lambda state, widget=self.tableWidget, target = self.target, e_widget=self.e_tableWidget: self.pushBt_improve_clicked(state, widget, target, e_widget))

    # 파일선택 버튼 클릭 함수
    def pushBt_file_chc_clicked(self, state, widget, announce, fileName, rows, columns, e_widget):
        # 파일 경로 추출
        fname = QFileDialog.getOpenFileName(self, '파일 열기', '', 'All File(*)', 'All Files(*.*)')
        if fname[0]:
            # 파일 읽어서 Dataframe 채우기
            df = pd.read_csv(fname[0], encoding='cp949', header=None)
            df = df.fillna("")                                  # nan -> "" 으로 변환
            # 파일 이름 추출 및 파일명 출력
            fileName.setText(ntpath.basename(fname[0]))
            # Table widget 알림말 제거
            announce.clear()
            # Table widget 구성
            self.create_table_widget(widget, df, e_widget)
            # 행, 열 갯수 출력
            rows.setText(str(widget.rowCount()-1))              # 첫 행은 제외
            columns.setText(str(widget.columnCount()))
        else:
            print("파일 안 골랐음")

    # TableWidget 구성 함수
    def create_table_widget(self, widget, df, e_widget):
        widget.setRowCount(len(df.index)+1)     # 첫 행에 Combobox 넣기 위해 행 갯수 1 늘림
        widget.setColumnCount(len(df.columns))
        widget.horizontalHeader().setDefaultSectionSize(200)    # 열 너비 고정
        e_widget.setRowCount(len(df.index) + 1)      # 첫 행에 Combobox 넣기 위해 행 갯수 1 늘림
        e_widget.setColumnCount(len(df.columns))
        e_widget.horizontalHeader().setDefaultSectionSize(200)    # 열 너비 고정
        # widget.setHorizontalHeaderLabels(df.columns)
        # widget.setVerticalHeaderLabels(df.index)
        for row_index, row in enumerate(df.index):      # 정비 진행할 TableWidget 생성 -> widget
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index+1, col_index, item)    # 첫 행 비워 놓고 데이터 채우기
        for row_index, row in enumerate(df.index):      # 비교 위한 백업용 TablWidget 생성 -> e_widget
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                e_widget.setItem(row_index+1, col_index, item)
        colcount = widget.columnCount()
        for i in range(0, colcount):
            locals()['cb{}'.format(i)] = QComboBox(self)    # 콤보박스 동적할당

            cb = locals()['cb{}'.format(i)]
            cb.addItem("문자열")
            cb.addItem("금액/수량/비율")
            cb.addItem("여부 > Y, N")
            cb.addItem("여부 > 남, 여")
            cb.addItem("날짜 > YYYY-MM-DD HH24:MI:SS")
            cb.addItem("날짜 > YYYY-MM-DD HH24:MI")
            cb.addItem("날짜 > YYYY-MM-DD HH24")
            cb.addItem("날짜 > YYYY-MM-DD")
            cb.addItem("날짜 > YYYY-MM")
            cb.addItem("날짜 > YYYY")
            cb.addItem("날짜 > MM")
            cb.addItem("날짜 > DD")
            cb.addItem("날짜 > MM-DD HH24:MI:SS")
            cb.addItem("날짜 > MM-DD HH24:MI")
            cb.addItem("날짜 > MM-DD")
            cb.addItem("날짜 > HH24:MI:SS")
            cb.addItem("날짜 > MI:SS")
            cb.addItem("날짜 > HH24:MI")
            cb.addItem("날짜 > HH24")
            cb.addItem("날짜 > MI")
            cb.addItem("날짜 > SS")
            cb.addItem("전화번호")
            cb.addItem("우편번호")
            cb.addItem("사업자번호")
            widget.setCellWidget(0, i, cb)

    def setting_red(self, e_widget, j, i, target_data, target):       # 진단 시 오류 값 다홍색으로 변경
        e_widget.item(j, i).setBackground(QtGui.QColor(255, 102, 102))
        if target_data not in target:
            target.append(target_data)
    def setting_white(self, e_widget, j, i, target_data, target):       # 재진단 시 정상 값 흰색으로 변경
        e_widget.item(j, i).setBackground(QtGui.QColor("white"))
        if target_data in target:
            target.remove(target_data)
    def setting_blue(self, widget, x, y):  # 정비 시 정비 완료된 셀 푸른색으로 변경
        widget.item(x, y).setBackground(QtGui.QColor(204, 255, 255))  # 해당 셀 배경색 푸른색으로 변경

    # 진단 버튼 클릭 함수
    def pushBt_diagnosis_clicked(self, state, widget, e_widget, target):
        widget.setFixedSize(1171,360)
        e_widget.show()
        # 열 개수 추출
        col_count = e_widget.columnCount()
        row_count = e_widget.rowCount()
        for i in range(0, col_count):     # 열 데이터 형태, 항목명 점검
            # 열 이름 하나씩 추출
            data = widget.item(1, i)
            cBox = widget.cellWidget(0, i).currentText()
            if data.text().encode().isalpha():      # 항목명이 영어로만 이루어져 있는지 판별
                e_widget.item(1, i).setBackground(QtGui.QColor(255, 102, 102))     # 해당 셀 배경색 주황색으로 변경
            for j in range(2, row_count):
                row_data = widget.item(j, i)
                target_data = [j, i]
                if row_data.text() == "":   # 모든 열에서 공백 허용
                    self.setting_white(e_widget, j, i, target_data, target)
                elif row_data.text() == "-" or row_data.text().isspace():    # 모든 열에서 "-", " " 값 비허용
                    self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "금액/수량/비율":    # "금액/수량/비율" 규칙 숫자 아닌 값 비허용
                    if not row_data.text().isdigit():
                        self.setting_red(e_widget, j, i, target_data, target)
                    else:
                        self.setting_white(e_widget, j, i, target_data, target)
                elif cBox == "여부 > Y, N":     # "여부 > Y, N" 규칙 "Y", "N" 아닌 값 비허용
                    if not row_data.text() == "Y" and not row_data.text() == "N":
                        self.setting_red(e_widget, j, i, target_data, target)
                    else:
                        self.setting_white(e_widget, j, i, target_data, target)
                elif cBox == "여부 > 남, 여":     # "남", "여" 아닌 값 비허용
                    if not row_data.text() == "남" and not row_data.text() == "여":
                        self.setting_red(e_widget, j, i, target_data, target)
                    else:
                        self.setting_white(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY-MM-DD HH24:MI:SS":      # 해당 날짜 형식이 아닌 값 비허용
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y-%m-%d %H:%M:%S")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY-MM-DD HH24:MI":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y-%m-%d %H:%M")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY-MM-DD HH24":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y-%m-%d %H")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY-MM-DD":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y-%m-%d")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY-MM":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y-%m")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > YYYY":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%Y")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > MM":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%m")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > DD":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%d")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > MM-DD HH24:MI:SS":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%m-%d %H:%M:%S")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > MM-DD HH24:MI":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%m-%d %H:%M")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > HH24:MI:SS":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%H:%M:%S")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > MI:SS":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%M:%S")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > HH24:MI":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%H:%M")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > HH24":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%H")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > MI":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%M")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "날짜 > SS":
                    try:
                        datetime.datetime.strptime(row_data.text(), "%S")
                        self.setting_white(e_widget, j, i, target_data, target)
                    except ValueError:
                        self.setting_red(e_widget, j, i, target_data, target)
                elif cBox == "전화번호":
                    if re.compile(r"\d{3}-\d{4}-\d{4}").match(row_data.text()) or re.compile(r"\d{3}-\d{3}-\d{4}").match(row_data.text()) or re.compile(r"\d{2}-\d{3}-\d{4}").match(row_data.text()) or re.compile(r"\d{2}-\d{4}-\d{4}").match(row_data.text()) or re.compile(r"\d{4}-\d{4}").match(row_data.text()):
                        self.setting_white(e_widget, j, i, target_data, target)
                    else:
                        self.setting_red(e_widget, j, i, target_data, target)

                elif cBox == "우편번호":
                    zip_code = df_postal.loc[df_postal['우편번호'] == int(row_data.text()), ['우편번호']].values
                    if str(zip_code) == '[]':
                        self.setting_red(e_widget, j, i, target_data, target)
                    else:
                        self.setting_white(e_widget, j, i, target_data, target)

        index = 0
        for z in target:    # 테스트용 출력
            print(str(index) + "번째 열 : " + str(z))
            index = index + 1

    # 재시작 버튼 클릭 함수
    def pushBt_restart_clicked(self, state, widget, announce, fileName, rows, columns, e_widget):
        widget.clear()
        widget.setRowCount(0)
        widget.setColumnCount(0)
        announce.setText("선택된 csv 파일이 없습니다.")
        fileName.clear()
        rows.clear()
        columns.clear()
        widget.setFixedSize(1171, 721)  # TableWidget 사이즈 원래대로
        e_widget.hide()     # 기존 비교 위한 TableWidget 숨김처리

    # 정비 버튼 클릭 함수
    def pushBt_improve_clicked(self, state, widget, target, e_widget):
        result = list()
        for target_data in target:
            x = target_data[0]      # 정비 대상 행 인덱스
            y = target_data[1]      # 정비 대상 열 인덱스
            cBox = widget.cellWidget(0, y).currentText()
            # 공통 부분
            if widget.item(x, y).text() == "-" or widget.item(x, y).text().isspace():  # 해당 셀 값이 스페이스 바 또는 - 인지 판별
                widget.setItem(x, y, QTableWidgetItem(""))  # 해당 셀 값 공백으로 변경
                self.setting_blue(widget, x, y)
                result.append(target_data)
            elif cBox == "금액/수량/비율":    # "금액/수량/비율" 규칙 숫자 아닌 값 비허용
                widget.setItem(x, y, QTableWidgetItem(re.sub(r'[^0-9]', '', widget.item(x, y).text())))
                self.setting_blue(widget, x, y)
                result.append(target_data)
            elif cBox == "여부 > Y, N":  # "여부 > Y, N" 규칙 "Y", "N" 아닌 값 비허용
                if widget.item(x, y).text() == "y":
                    widget.setItem(x, y, QTableWidgetItem("Y"))
                    self.setting_blue(widget, x, y)
                    result.append(target_data)
                elif widget.item(x, y).text() == "n":
                    widget.setItem(x, y, QTableWidgetItem("N"))
                    self.setting_blue(widget, x, y)
                    result.append(target_data)
                else:
                    widget.item(x, y).setBackground(QtGui.QColor(255, 102, 102))
            elif cBox == "전화번호":
                number = re.sub(r'[^0-9]', '', widget.item(x, y).text())
                phone_no = ""
                if len(number) == 8:
                    for i in range(len(number)):
                        phone_no += number[i]
                        if i == 3:
                            phone_no += "-"
                elif len(number) == 9:
                    for i in range(len(number)):
                        phone_no += number[i]
                        if i == 1 or i == 4:
                            phone_no += "-"
                elif len(number) == 10:
                    if number[0] == "0" and number[1] == "2":
                        for i in range(len(number)):
                            phone_no += number[i]
                            if i == 1 or i == 5:
                                phone_no += "-"
                    else:
                        for i in range(len(number)):
                            phone_no += number[i]
                            if i == 2 or i == 5:
                                phone_no += "-"
                elif len(number) == 11:
                    for i in range(len(number)):
                        phone_no += number[i]
                        if i == 2 or i == 6:
                            phone_no += "-"
                print(phone_no)
                if re.compile(r"\d{3}-\d{4}-\d{4}").match(phone_no) or re.compile(r"\d{3}-\d{3}-\d{4}").match(phone_no) or re.compile(r"\d{2}-\d{3}-\d{4}").match(phone_no) or re.compile(r"\d{2}-\d{4}-\d{4}").match(phone_no) or re.compile(r"\d{4}-\d{4}").match(phone_no):
                    widget.setItem(x, y, QTableWidgetItem(phone_no))
                    self.setting_blue(widget, x, y)
                    result.append(target_data)
                else:
                    widget.item(x, y).setBackground(QtGui.QColor(255, 102, 102))
        print(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()