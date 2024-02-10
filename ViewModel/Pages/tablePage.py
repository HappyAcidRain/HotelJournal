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
        self.setupUi(self)

        self.btn_save.clicked.connect(self.save)
        self.btn_export.clicked.connect(self.export)

        self.reportSave = saveAndLoad.TableSave()
        self.reportSave.s_data.connect(self.save_dialog)

        self.reportExport = tableExport

        self.reportRead = saveAndLoad.TableRead()
        self.reportRead.finished.connect(lambda: self.reportSum.start())
        self.reportRead.s_data.connect(self.write)

    def start(self):
        self.reportSum.set(self.tw_reportTable)
        self.tw_reportTable.cellChanged.connect(self.calculate)

    def set(self, table_name, cal_table):
        self.table_name = table_name
        self.calTable = cal_table

        self.set_table()
        self.insert_dates()
        self.set_sum_row()
        self.read()

    def insert_dates_and_days(self):

        min_day, min_month, max_day, max_month = [None, None, None, None]  # placeholder
        # insert dates in table

        if self.tw_reportTable.rowCount() - 1 == 1:
            self.tw_reportTable.setRowCount(3)

        else:
            self.tw_reportTable.setRowCount(self.tw_reportTable.rowCount() + 1)

        row = self.tw_reportTable.rowCount() - 1
        text = f"{min_day}.{min_month} - {max_day}.{max_month}"

        self.write(row, 0, text)

        # insert days in table

        cur_year = QDate().currentDate().year()
        min_date = QDate(cur_year, min_month, min_day)
        max_date = QDate(cur_year, max_month, max_day)
        days = str(max_date.dayOfYear() - min_date.dayOfYear())

        if days == '0':
            self.write(row, 1, '1')
        else:
            self.write(row, 1, days)


    def save(self):
        self.saveDialog.set_range(self.tw_reportTable.rowCount() * self.tw_reportTable.columnCount())
        self.saveDialog.show()
        self.reportSave.set(self.tw_reportTable, '_' + self.table_name)
        self.reportSave.start()

    def read(self):
        self.reportRead.set('_' + self.table_name, self.tw_reportTable)
        self.reportRead.start()

    def export_dialog(self):   # TODO: add file dialog
        # self.path = QFileDialog.getOpenFileUrl()
        pass

    def export(self):
        msg = self.reportExport.export(self.tw_reportTable)
        if msg:
            self.animations.PopUpAnimation()
