from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize, Qt, QDate
from PyQt6.QtWidgets import QDialog, QColorDialog

from Views.Dialogs import editDialogUI


class EditDialog(QDialog, editDialogUI.Ui_Dialog, QSize):
    s_info = QtCore.pyqtSignal(int, int, int, int, int, str)  # row, column, color(r, g, b), note

    def __init__(self):
        super(EditDialog, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon(f'View/assets/icon96px.ico'))
        self.setWindowTitle("Редактирование")
        self.setFixedSize(QSize(370, 430))

        self.date_in.setDate(QDate.currentDate())
        self.date_out.setDate(QDate.currentDate())

        self.btn_color.clicked.connect(self.colorDialog)
        self.btn_save.clicked.connect(self.save)

        self.color = None
        self.notes = None

    def setStyle(self, style):
        self.setStyleSheet(style)

    def colorDialog(self):
        self.color = QColorDialog.getColor()

    def save(self):
        notes = self.te_notes.toPlainText()
        timeIn = self.time_in.time().toString(Qt.DateFormat.ISODate)
        timeOut = self.time_out.time().toString(Qt.DateFormat.ISODate)

        notes = f"Заезд: {timeIn}\nВыезд: {timeOut}\n\n{notes}"

        day_out = self.date_out.date().dayOfYear()
        month_count = self.date_in.date()
        day = self.date_in.date().day()
        cur_day = self.date_in.date()
        added_months = 0
        added_days = 0

        workie = True

        while workie:

            if cur_day.dayOfYear() <= day_out:

                if day <= month_count.daysInMonth():
                    month = month_count.month()

                    if self.color is not None:
                        red, green, blue, _ = self.color.getRgb()
                    else:
                        red, green, blue = (100, 100, 150)

                    self.s_info.emit(month - 1, day - 1, red, green, blue, notes)
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
                workie = False
