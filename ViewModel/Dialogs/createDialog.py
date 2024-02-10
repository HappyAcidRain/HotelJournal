from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QSize

import sqlite3

from Views.Dialogs import createDialogUI


class CreateDialog(QDialog, createDialogUI.Ui_Dialog, QSize):
    s_upd = QtCore.pyqtSignal()

    def __init__(self):
        super(CreateDialog, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('Views/assets/icon96px.ico'))
        self.setWindowTitle("Создать новую таблицу")
        self.setFixedSize(QSize(350, 110))

        self.btn_create.clicked.connect(self.emit_name)

    def emit_name(self):  # ! put in model
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        name = self.le_name.text()

        if name != '':
            report_name = '_' + name

            try:
                cursor.execute(f"""CREATE TABLE {name} (
                        date         TEXT    UNIQUE,
                        notes        TEXT,
                        color        TEXT
                    );""")

                cursor.execute(f"""CREATE TABLE {report_name} (
                        date        TEXT    UNIQUE,
                        price       INTEGER,
                        sum         INTEGER,
                        rent        INTEGER,
                        guest       INTEGER,
                        avito       INTEGER,
                        expense     INTEGER,
                        indications TEXT,
                        income      INTEGER                 
                    );""")

                connect.commit()
                connect.close()

                self.s_upd.emit()
                self.close()

            except sqlite3.OperationalError:
                self.alert("Невозможно создать таблицу с эти именем!",
                           "Возможно, таблица с эти именем уже существет, " +
                           "либо имя содержит недопустимые символы.")

        else:
            self.alert("Вы не ввели имя таблицы!", "")

    def alert(self, text, info_text):
        msg = QMessageBox(text=text, parent=self)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setInformativeText(info_text)
        msg.setIcon(QMessageBox.Icon.Critical)
        ret = msg.exec()
