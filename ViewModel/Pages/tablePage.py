from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from Views.Pages import tableUI
from Model import saveAndLoad
from Model import tableExport


class ReportPage(QMainWindow, tableUI.Ui_MainWindow, QDate):
    def __init__(self):
        super(ReportPage, self).__init__()
        self.setupUi(self)
        self.calTable = None
        self.table_name = None

        self.btn_save.clicked.connect(self.save)
        self.btn_export.clicked.connect(self.export)

        self.reportSave = saveAndLoad.TableSave()
        self.reportSave.s_data.connect(self.save_dialog)

        self.reportExport = tableExport

        self.reportRead = saveAndLoad.TableRead()
        self.reportRead.finished.connect(lambda: self.reportSum.start())
        self.reportRead.s_data.connect(self.write)
        self.reportRead.w_data.connect(self.write_dates_and_days)

    def start(self):
        self.reportSum.set(self.tw_reportTable)
        self.tw_reportTable.cellChanged.connect(self.calculate)

    def set(self, table_name, cal_table):
        self.table_name = table_name
        self.calTable = cal_table

        self.reportRead.set(table_name, cal_table)
        self.set_table()
        self.reportRead.insert_dates()
        self.set_sum_row()
        self.read()

    def write_dates_and_days(self, min_day, min_month, max_day, max_month, days_count):
        if self.tw_reportTable.rowCount() - 1 == 1:
            self.tw_reportTable.setRowCount(3)

        else:
            self.tw_reportTable.setRowCount(self.tw_reportTable.rowCount() + 1)

        row = self.tw_reportTable.rowCount() - 1
        text = f"{min_day}.{min_month} - {max_day}.{max_month}"

        self.write(row, 0, text)
        self.write(row, 1, days_count)

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
