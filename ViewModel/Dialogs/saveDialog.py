from PyQt6 import QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog

from Views.Dialogs import saveDialogUI


class SaveDialog(QDialog, saveDialogUI.Ui_Dialog, QSize):
    def __init__(self):
        super(SaveDialog, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon(f'Views/assets/icon96px.ico'))
        self.setWindowTitle("Сохранение")
        self.setFixedSize(QSize(400, 84))

    def set_range(self, range_):
        self.pb_save.setRange(0, range_)

    def add(self):
        self.pb_save.setValue(self.pb_save.value() + 1)
