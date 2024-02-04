from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize, QDate

from Views.Dialogs import deleteDialogUI


class DeleteDialog(QDialog, deleteDialogUI.Ui_Dialog, QSize):
    s_cords = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(DeleteDialog, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon(f'Views/assets/icon96px.ico'))
        self.setWindowTitle("Редактирование")
        self.setFixedSize(QSize(302, 170))

        self.date_in.setDate(QDate.currentDate())
        self.date_out.setDate(QDate.currentDate())

        self.btn_cancel.clicked.connect(lambda: self.close())
        self.btn_del.clicked.connect(self.delete)

    def delete(self):
        day_out = self.date_out.date().dayOfYear()
        month_count = self.date_in.date()
        day = self.date_in.date().day()
        cur_day = self.date_in.date()
        added_months = 0
        added_days = 0

        while True:

            if cur_day.dayOfYear() <= day_out:

                if day <= month_count.daysInMonth():
                    month = month_count.month()
                    self.s_cords.emit(month - 1, day - 1)
                    day += 1
                    added_days += 1
                    cur_day = self.date_in.date().addDays(added_days)

                else:
                    day = 1
                    added_months += 1
                    month_count = self.date_in.date().addMonths(added_months)

            else:
                month_count = self.date_in.date()
                day = self.date_in.date().day()
                cur_day = self.date_in.date()
                added_months = 0
                added_days = 0
                break

    def setStyle(self, style_sheet):
        self.setStyleSheet(style_sheet)
