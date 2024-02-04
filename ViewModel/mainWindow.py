from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from Model import cloudUpload

from Views import mainUI

from ViewModel.Dialogs import deleteDialog
from ViewModel.Dialogs import saveDialog
from ViewModel.Dialogs import editDialog
from ViewModel.Dialogs import createDialog

from ViewModel.Pages import calendarPage
from ViewModel.Pages import tablePage

import sqlite3


class MainWindow(QMainWindow, mainUI.Ui_MainWindow, QDialog, QColor, QSize, QSizePolicy, QHeaderView, QGridLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon96px.ico'))
        self.setWindowTitle("BusinessThing")
        self.statusbar.showMessage("ver 1.3")
        self.resizeable()
        self.set_actions()
        self.fetch_tables()

        self.deleteDialog = deleteDialog.DeleteDialog()
        self.saveDialog = saveDialog.SaveDialog()
        self.editDialog = editDialog.EditDialog()

        self.createDialog = createDialog.CreateDialog()
        self.createDialog.s_upd.connect(self.update_table_list)

        self.calendarPage = calendarPage.CalendarPage()
        self.calendarPage.s_saveFinished.connect(self.report_open)
        self.calendarPage.resizeable()

        self.reportPage = tablePage.ReportPage()
        self.reportPage.resizeable()

        self.theme = "Light"
        self.reportOpenAllow = False
        self.set_tab_bar(self.tb_main)
        self.setTheme()

    def set_tab_bar(self, tab_bar):
        tab_bar.addTab(self.calendarPage, "Календарь")
        tab_bar.addTab(self.reportPage, "Отчёт")

        tab_bar.setTabIcon(0, QIcon("assets/left-dark-arrow-50.png"))  # placeholder
        tab_bar.setTabIcon(1, QIcon("assets/right-dark-arrow-50.png"))  # placeholder
        tab_bar.tabBarClicked.connect(self.report)
        tab_bar.setCurrentIndex(2)

    def set_actions(self):
        self.change_menu = QMenu('сменить таблицу', self)

        self.load_act = QAction('Загрузить', self)
        self.saveAct = QAction('Сохранить', self)
        self.createAct = QAction('Создать', self)
        self.uploadAct = QAction('Сохранить в облаке', self)
        self.m_file.addAction(self.createAct)
        self.m_file.addAction(self.saveAct)
        self.m_file.addAction(self.load_act)
        self.m_file.addAction(self.uploadAct)

        self.themeAct = QAction('Сменить тему', self)
        self.m_settings.addAction(self.themeAct)

        self.themeAct.triggered.connect(self.setTheme)
        self.saveAct.triggered.connect(self.page_save)
        self.load_act.triggered.connect(self.page_read)
        self.uploadAct.triggered.connect(lambda: cloudUpload.upload())
        self.createAct.triggered.connect(lambda: self.createDialog.show())

    def setTheme(self):
        if self.theme == "Light":
            with open('Views/Themes/lightDefault/main.css') as file:
                style = file.read()
                self.setStyleSheet(style)

            with open('Views/Themes/lightDefault/report.css') as file:
                style = file.read()
                self.reportPage.setStyleSheet(style)

            with open('Views/Themes/lightDefault/calendar.css') as file:
                style = file.read()
                self.calendarPage.setStyleSheet(style)

            with open('Views/Themes/lightDefault/std.css') as file:
                style = file.read()
                self.createDialog.setStyleSheet(style)
                self.calendarPage.setStyle(style)

            self.theme = "Dark"

        else:
            with open('Views/Themes/darkDefault/main.css') as file:
                style = file.read()
                self.setStyleSheet(style)

            with open('Views/Themes/darkDefault/report.css') as file:
                style = file.read()
                self.reportPage.setStyleSheet(style)

            with open('Views/Themes/darkDefault/calendar.css') as file:
                style = file.read()
                self.calendarPage.setStyleSheet(style)

            with open('Views/Themes/darkDefault/std.css') as file:
                style = file.read()
                self.createDialog.setStyleSheet(style)
                self.calendarPage.setStyle(style)

            self.theme = "Light"

    def resizeable(self):
        sizePolicy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Expanding,
                                           QSizePolicy.Policy.Expanding)
        self.tb_main.setSizePolicy(sizePolicy)
        self.setCentralWidget(self.tb_main)

    def page_save(self):
        page = self.tb_main.currentIndex()
        if page == 0:
            self.calendarPage.save()

        else:
            self.reportPage.save()

    def page_read(self):
        page = self.tb_main.currentIndex()
        if page == 0:
            self.calendarPage.read()

        else:
            self.reportPage.read()

    def fetch_tables(self):

        def make_act(name, item):
            self.name = QAction(str(item), self)
            self.change_menu.addAction(self.name)
            self.name.triggered.connect(lambda: table_change(item))

        def table_change(name):
            self.calendarPage.tableName = str(name)

            # сброс таблицы
            self.calendarPage.tw_table.setRowCount(0)
            self.calendarPage.tw_table.setColumnCount(0)
            self.calendarPage.set_table()

            self.calendarPage.read()

        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        tableList = cursor.fetchall()

        indexCount = 0

        for item in tableList:

            clearItem = ""
            for i in item:
                clearItem += str(i)

            tableList[indexCount] = clearItem

            if '_' in clearItem:
                indexCount += 1

            else:
                make_act(f"{tableList[indexCount]}Act", tableList[indexCount])
                self.m_file.addMenu(self.change_menu)
                indexCount += 1

        indexCount = 0

    def update_table_list(self):
        self.change_menu.clear()
        self.fetch_tables()

    def report(self):
        if self.tb_main.currentIndex() == 0:
            self.calendarPage.save()
            self.reportOpenAllow = True

    def report_open(self, save_finished):
        calendar = self.calendarPage
        report = self.reportPage

        if self.reportOpenAllow and save_finished:
            report.set(calendar.tw_table, calendar.tableName)
            report.start()
            self.reportOpenAllow = False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())