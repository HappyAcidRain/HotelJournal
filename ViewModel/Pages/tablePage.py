from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from Views.Pages import tableUI
from ViewModel.Threads import sumTableThread
from ViewModel.Dialogs import saveDialog

from Model import saveAndLoad
from Model import tableExport

import sqlite3


class ReportPage(QMainWindow, tableUI.Ui_MainWindow, QDate):
    def __init__(self):
        super(ReportPage, self).__init__()
        self.colorVariations = None
        self.reportRead = None
        self.setupUi(self)
        self.calTable = None
        self.tableName = None
        self.path = None
        self.totalList = []

        self.btn_save.clicked.connect(self.save)
        self.btn_export.clicked.connect(self.export)

        self.reportSave = saveAndLoad.SaveReportThread()
        self.reportSave.s_updPB.connect(self.save_dialog)

        self.reportSum = sumTableThread.SumReportThread()
        self.reportSum.s_sumData.connect(self.change_sum_row)

        self.reportExport = tableExport

        self.saveDialog = saveDialog.SaveDialog()

    def start(self):

        self.setTable()
        self.insert_dates()
        self.setSumRow()

        self.reportRead = saveAndLoad.ReadReportThread()
        self.reportRead.set('_' + self.tableName, self.tw_reportTable)
        self.reportRead.finished.connect(lambda: self.reportSum.start())
        self.reportRead.s_readData.connect(self.write)
        self.reportRead.start()

        self.reportSum.set(self.tw_reportTable)
        self.tw_reportTable.cellChanged.connect(self.calculate)

    def change_sum_row(self, total):

        last_row = self.tw_reportTable.rowCount() - 1
        alignment = QtCore.Qt.AlignmentFlag.AlignCenter

        self.totalList.append(total)

        if len(self.totalList) == 4:
            column = 4
            for item in self.totalList:
                cell = self.tw_reportTable.item(last_row, column)
                cell.setText(str(item))
                cell.setTextAlignment(alignment)

                if column < 6:
                    column += 1
                else:
                    column = 9

            self.totalList.clear()

    def set(self, cal_table, table_name):
        self.calTable = cal_table
        self.tableName = table_name

    def color(self, row, column):

        colors = ((191, 255, 172), (255, 219, 224), (249, 211, 249),
                  (249, 211, 249), (243, 243, 155), (255, 237, 178),
                  (202, 199, 248))

        match column:

            case 4:
                if row == 0:
                    red, green, blue = colors[0]
                    cell = self.tw_reportTable.item(row, column)
                    cell.setBackground(QtGui.QColor(red, green, blue))

                else:
                    red, green, blue = colors[1]
                    cell = self.tw_reportTable.item(row, column)
                    cell.setBackground(QtGui.QColor(red, green, blue))

            case 5:
                red, green, blue = colors[2]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 6:
                red, green, blue = colors[3]
                cell = self.tw_reportTable.item(row, column)

                cell.setBackground(QtGui.QColor(red, green, blue))

            case 7:
                red, green, blue = colors[4]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 8:
                red, green, blue = colors[5]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 9:
                red, green, blue = colors[6]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

    def write(self, row, column, text):
        alignment = QtCore.Qt.AlignmentFlag.AlignCenter
        self.tw_reportTable.setItem(row, column, QTableWidgetItem())
        self.tw_reportTable.item(row, column).setText(text)
        self.tw_reportTable.item(row, column).setTextAlignment(alignment)

        self.color(row, column)

    def insert_dates(self):

        # fetching dates
        self.colorVariations = []

        for column in range(self.calTable.columnCount()):

            for row in range(self.calTable.rowCount()):
                cell = self.calTable.item(row, column)

                if cell:

                    red, green, blue, _ = cell.background().color().getRgb()
                    color = f"{red}:{green}:{blue}"

                    if color != None:
                        self.colorVariations.append(color)
                        self.colorVariations.sort()

                        self.colorVariations = list(dict.fromkeys(self.colorVariations))

        for color in self.colorVariations:
            connect = sqlite3.connect("Model/Database/people.db")
            cursor = connect.cursor()

            cursor.execute(f"""SELECT month FROM {self.tableName} WHERE color = '{color}'""")
            DBmonth = cursor.fetchall()
            DBmonth.sort()

            index = 0
            for item in DBmonth:

                monthTemp = ""
                for i in item:
                    monthTemp += str(i)
                month = int(monthTemp)

                DBmonth[index] = month
                index += 1

            DBmonth = list(dict.fromkeys(DBmonth))

            dayList = []

            for month in DBmonth:
                cursor.execute(f"""SELECT day FROM {self.tableName} WHERE month = {month} AND color = '{color}'""")
                DBday = cursor.fetchall()

                index = 0
                for item in DBday:

                    dayTemp = ""
                    for i in item:
                        dayTemp += str(i)
                    day = int(dayTemp) + 1

                    DBday[index] = day
                    index += 1

                dayList.append(DBday)

            minDay = dayList[0][0]  # FIX: IndexError: list index out of range
            maxDay = dayList[-1][-1]

            minMonth = DBmonth[0] + 1
            maxMonth = DBmonth[-1] + 1

            # insert dates in table

            if self.tw_reportTable.rowCount() - 1 == 1:
                self.tw_reportTable.setRowCount(3)

            else:
                self.tw_reportTable.setRowCount(self.tw_reportTable.rowCount() + 1)

            row = self.tw_reportTable.rowCount() - 1
            text = f"{minDay}.{minMonth} - {maxDay}.{maxMonth}"

            self.write(row, 0, text)

            # insert days in table

            cur_year = QDate().currentDate().year()
            min_date = QDate(cur_year, minMonth, minDay)
            max_date = QDate(cur_year, maxMonth, maxDay)
            days = str(max_date.dayOfYear() - min_date.dayOfYear())

            if days == '0':
                self.write(row, 1, '1')
            else:
                self.write(row, 1, days)

    def calculate(self, row, column):
        if column == 2:
            entered = self.tw_reportTable.currentItem()

            if entered and entered.text().isdigit():
                days = self.tw_reportTable.item(row, 1).text()
                self.write(row, 3, str(int(entered.text()) * int(days)))

        elif column == 4 or 5 or 6 or 9:
            self.reportSum.start()

    def save(self):
        self.saveDialog.set_range(self.tw_reportTable.rowCount() * self.tw_reportTable.columnCount())
        self.saveDialog.show()

        self.reportSave.set(self.tw_reportTable, '_' + self.tableName)
        self.reportSave.start()

    def save_dialog(self, msg):
        if msg == 'upd':
            self.saveDialog.add()
        else:
            self.saveDialog.close()

    def export_dialog(self):   # ! add file dialog
        # self.path = QFileDialog.getOpenFileUrl()
        pass

    def export(self):
        msg = self.reportExport.export(self.tw_reportTable)
        if msg:
            self.animations.PopUpAnimation()
