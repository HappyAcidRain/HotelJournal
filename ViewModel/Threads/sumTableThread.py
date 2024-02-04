from PyQt6 import QtCore
from PyQt6.QtCore import QThread


class SumReportThread(QThread):
    s_sumData = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.columnList = [4, 5, 6, 9]
        self.table = None

    def set(self, table):
        self.table = table

    def run(self):
        for column in self.columnList:
            row = self.table.rowCount() - 2
            total = 0

            for row in range(row):
                if row != 0:
                    item = self.table.item(row, column)
                    if item and item.text().isdigit():
                        total += int(item.text())

            self.s_sumData.emit(total)
