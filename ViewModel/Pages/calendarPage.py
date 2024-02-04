from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDialog, QSizePolicy, QHeaderView, QMainWindow, QGridLayout, QTableWidgetItem
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from ViewModel.Dialogs import editDialog, deleteDialog, saveDialog
from Views.Pages import calendarUI
from Model import saveAndLoad


class CalendarPage(QMainWindow, calendarUI.Ui_MainWindow, QDialog,
                   QColor, QSize, QSizePolicy, QHeaderView,QGridLayout):
    s_saveFinished = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(CalendarPage, self).__init__()
        self.setupUi(self)

        self.tableName = "DefaultTable"
        self.reportOpenAllow = False

        self.tw_table.cellDoubleClicked.connect(lambda: self.deleteDialog.show())
        self.tw_table.cellClicked.connect(lambda: self.editDialog.show())
        self.btn_notes.clicked.connect(lambda: self.editDialog.show())
        self.btn_del.clicked.connect(lambda: self.deleteDialog.show())
        self.btn_save.clicked.connect(self.save)

        self.readThread = saveAndLoad.ReadThread()
        self.readThread.s_data.connect(self.write)

        self.saveThread = saveAndLoad.SaveThread()
        self.saveThread.s_update.connect(self.saving_dialog)
        self.saveThread.finished.connect(lambda: self.s_saveFinished.emit(True))

        self.editDialog = editDialog.EditDialog()
        self.editDialog.s_info.connect(self.write)

        self.deleteDialog = deleteDialog.DeleteDialog()
        self.deleteDialog.s_cords.connect(self.clear)

        self.saveDialog = saveDialog.SaveDialog()

        self.set_table()
        self.read()

    def resizeable(self):

        ver_layout = QVBoxLayout()
        hor_layout = QHBoxLayout()

        btn_list = [self.btn_del, self.btn_notes, self.btn_save]

        for button in btn_list:
            hor_layout.addWidget(button)
            button.setMinimumSize(QSize(130, 30))

        hor_layout.insertStretch(1, 500)

        ver_layout.addWidget(self.tw_table)
        size_policy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tw_table.setSizePolicy(size_policy)

        ver_layout.addLayout(hor_layout)
        self.centralwidget.setLayout(ver_layout)

    def setStyle(self, style):
        self.editDialog.setStyleSheet(style)
        self.deleteDialog.setStyleSheet(style)
        self.saveDialog.setStyleSheet(style)

    def set_table(self):

        self.tw_table.setRowCount(12)
        self.tw_table.setColumnCount(31)

        for i in range(31):
            self.tw_table.setColumnWidth(i, 20)

        self.tw_table.setLineWidth(10)

        month_tuple = (
            'Январь', 'Февраль', 'Март',
            'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь',
            'Октябрь', 'Ноябрь', 'Декабрь',
        )

        self.tw_table.setVerticalHeaderLabels(month_tuple)

        ver_header = self.tw_table.verticalHeader()
        hor_header = self.tw_table.horizontalHeader()

        for i in range(self.tw_table.rowCount()):
            ver_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        for i in range(self.tw_table.columnCount()):
            hor_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # ver_header.setDefaultAlignment(QtCore.Qt.AlignCenter) #TODO: Fix that
        # hor_header.setDefaultAlignment(QtCore.Qt.AlignCenter) #TODO: n' that

    def saving_dialog(self, msg):
        if msg == 'upd':
            self.saveDialog.add()
        else:
            self.saveDialog.close()

    def save(self):
        self.saveDialog.show()
        self.saveDialog.set_range(self.tw_table.columnCount() * self.tw_table.rowCount())

        self.saveThread.set(self.tableName, self.tw_table)
        self.saveThread.start()

    def read(self):
        self.readThread.set(self.tableName)
        self.readThread.start()

    def write(self, row, column, red, green, blue, notes):
        self.tw_table.setItem(row, column, QTableWidgetItem())

        if red is not None:
            self.tw_table.item(row, column).setBackground(QtGui.QColor(red, green, blue))

        if notes is not None:
            self.tw_table.item(row, column).setToolTip(notes)

    def clear(self, row, column):
        self.tw_table.setItem(row, column, None)
