from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from Model import cloudUpload, saveAndLoad
from Views import mainUI
from ViewModel.Dialogs import deleteDialog, saveDialog, editDialog, createDialog
from ViewModel.Pages import calendarPage, tablePage


import sqlite3


class MainWindow(QMainWindow, mainUI.Ui_MainWindow, QDialog, QColor, QSize, QSizePolicy, QHeaderView, QGridLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.resizeable()
        self.set_actions()
        self.fetch_tables()

        self.tableRead = saveAndLoad.TableRead()

        self.deleteDialog = deleteDialog.DeleteDialog()
        self.saveDialog = saveDialog.SaveDialog()
        self.editDialog = editDialog.EditDialog()

        self.createDialog = createDialog.CreateDialog()
        self.createDialog.s_upd.connect(self.update_table_list)

        self.calendarPage = calendarPage.CalendarPage()
        self.calendarPage.s_saveFinished.connect(self.report_open)
        self.calendarPage.resizeable()

        self.tablePage = tablePage.ReportPage()
        self.tablePage.resizeable()

        self.theme = "Light"
        self.reportOpenAllow = False
        self.set_tab_bar(self.tb_main)
        self.set_theme()

    def set_tab_bar(self, tab_bar):
        tab_bar.addTab(self.calendarPage, "Календарь")
        tab_bar.addTab(self.tablePage, "Отчёт")

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

        self.themeAct.triggered.connect(self.set_theme)
        self.saveAct.triggered.connect(self.page_save)
        self.load_act.triggered.connect(self.page_read)
        self.uploadAct.triggered.connect(lambda: cloudUpload.upload())
        self.createAct.triggered.connect(lambda: self.createDialog.show())

    def set_theme(self):
        if self.theme == "Light":
            with open('Views/Themes/lightDefault/main.css') as file:
                style = file.read()
                self.setStyleSheet(style)

            with open('Views/Themes/lightDefault/report.css') as file:
                style = file.read()
                self.tablePage.setStyleSheet(style)

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
                self.tablePage.setStyleSheet(style)

            with open('Views/Themes/darkDefault/calendar.css') as file:
                style = file.read()
                self.calendarPage.setStyleSheet(style)

            with open('Views/Themes/darkDefault/std.css') as file:
                style = file.read()
                self.createDialog.setStyleSheet(style)
                self.calendarPage.setStyle(style)

            self.theme = "Light"

    def resizeable(self):
        size_policy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Expanding,
                                            QSizePolicy.Policy.Expanding)
        self.tb_main.setSizePolicy(size_policy)
        self.setCentralWidget(self.tb_main)

    def page_save(self):
        page = self.tb_main.currentIndex()
        if page == 0:
            self.calendarPage.save()

        else:
            self.tablePage.save()

    def page_read(self):
        page = self.tb_main.currentIndex()
        if page == 0:
            self.calendarPage.read()
        else:
            self.tablePage.read()

    def fetch_tables(self):

        def make_act(name, item):
            self.name = QAction(str(item), self)
            self.change_menu.addAction(self.name)
            self.name.triggered.connect(lambda: table_change(item))

        def table_change(name):
            self.calendarPage.tableName = str(name)

            # table drop
            self.calendarPage.tw_table.setRowCount(0)
            self.calendarPage.tw_table.setColumnCount(0)
            self.calendarPage.set_table()

            self.calendarPage.read()

        table_list = saveAndLoad.CalendarRead.get_tables()

        index_count = 0

        for item in table_list:

            clear_item = ""
            for i in item:
                clear_item += str(i)

            table_list[index_count] = clear_item

            if '_' in clear_item:
                index_count += 1

            else:
                make_act(f"{table_list[index_count]}Act", table_list[index_count])
                self.m_file.addMenu(self.change_menu)
                index_count += 1

        index_count = 0

    def update_table_list(self):
        self.change_menu.clear()
        self.fetch_tables()

    def report(self):
        if self.tb_main.currentIndex() == 0:
            self.calendarPage.save()
            self.reportOpenAllow = True

    def report_open(self, save_finished):
        calendar = self.calendarPage
        report = self.tablePage

        if self.reportOpenAllow and save_finished:
            report.set(calendar.tableName, calendar.tw_table)
            report.start()
            self.reportOpenAllow = False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())
