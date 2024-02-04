from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 523)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tw_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tw_table.setGeometry(QtCore.QRect(10, 10, 911, 441))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_table.sizePolicy().hasHeightForWidth())

        self.tw_table.setSizePolicy(sizePolicy)
        self.tw_table.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tw_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tw_table.setObjectName("tw_table")
        self.tw_table.setColumnCount(0)
        self.tw_table.setRowCount(0)
        self.tw_table.horizontalHeader().setCascadingSectionResizes(True)
        self.tw_table.horizontalHeader().setStretchLastSection(False)
        self.tw_table.verticalHeader().setCascadingSectionResizes(True)
        self.tw_table.verticalHeader().setStretchLastSection(False)

        self.btn_notes = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_notes.setGeometry(QtCore.QRect(670, 460, 121, 31))
        self.btn_notes.setObjectName("btn_notes")

        self.btn_save = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(800, 460, 121, 31))
        self.btn_save.setObjectName("btn_save")

        self.btn_del = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_del.setGeometry(QtCore.QRect(550, 460, 113, 31))
        self.btn_del.setObjectName("btn_del")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_notes.setText(_translate("MainWindow", "добавить"))
        self.btn_save.setText(_translate("MainWindow", "сохранить"))
        self.btn_del.setText(_translate("MainWindow", "удалить"))
