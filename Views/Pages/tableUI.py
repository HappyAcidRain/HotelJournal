from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView


class Animations:
    def __init__(self, frame):
        self.heightSteps = None
        self.width = None
        self.frame = frame

        self.timer = QTimer()
        self.popUp = QPropertyAnimation(self.frame, b"pos")
        self.hide = QPropertyAnimation(self.frame, b"pos")

        self.timer.setSingleShot(True)
        self.timer.setInterval(2000)

        self.popUp.finished.connect(lambda: self.timer.start())
        self.timer.timeout.connect(self.hideAnimation)

    def setScreenSize(self, width, height):
        self.width = width
        # 40px - height of frame
        self.heightSteps = [
            int(height - 40),
            int(height - 58),
            int(height - 48)]

    def PopUpAnimation(self):  # * entry point for animation
        self.popUp.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.popUp.setKeyValueAt(0.1, QPoint(self.width, self.heightSteps[0]))
        self.popUp.setKeyValueAt(0.2, QPoint(self.width, self.heightSteps[1]))
        self.popUp.setEndValue(QPoint(self.width, self.heightSteps[2]))
        self.popUp.setDuration(500)
        self.popUp.start()

    def hideAnimation(self):
        self.hide.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.hide.setStartValue(QPoint(self.width, self.heightSteps[2]))
        self.hide.setEndValue(QPoint(self.width, self.heightSteps[0] + 200))
        self.hide.setDuration(500)
        self.hide.start()


class Ui_MainWindow(object):
    resized = QtCore.pyqtSignal()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 495)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tw_reportTable = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tw_reportTable.setGeometry(QtCore.QRect(0, 0, 1011, 451))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_reportTable.sizePolicy().hasHeightForWidth())

        self.tw_reportTable.setSizePolicy(sizePolicy)
        self.tw_reportTable.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tw_reportTable.setObjectName("tw_reportTable")
        self.tw_reportTable.setColumnCount(0)
        self.tw_reportTable.setRowCount(0)

        self.btn_save = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(890, 460, 121, 31))
        self.btn_save.setObjectName("btn_save")

        self.btn_export = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_export.setGeometry(QtCore.QRect(770, 460, 121, 31))
        self.btn_export.setObjectName("btn_export")

        self.f_msg = QtWidgets.QFrame(parent=self.centralwidget)
        self.f_msg.setGeometry(QtCore.QRect(340, 440, 300, 40))
        self.f_msg.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.f_msg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.f_msg.setObjectName("f_msg")

        self.lbl_msg = QtWidgets.QLabel(parent=self.f_msg)
        self.lbl_msg.setGeometry(QtCore.QRect(0, 0, 300, 40))
        self.lbl_msg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_msg.setObjectName("lbl_msg")

        self.animations = Animations(frame=self.f_msg)
        self.resized.connect(self.frameReposition)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_save.setText(_translate("MainWindow", "Сохранить"))
        self.btn_export.setText(_translate("MainWindow", "Экспорт"))
        self.lbl_msg.setText(_translate("MainWindow", "Таблица экспортирована!"))

    def setSumRow(self):
        if self.tw_reportTable.item(self.tw_reportTable.rowCount() - 1, 0) != None:

            lastRow = self.tw_reportTable.rowCount() + 1
            self.tw_reportTable.setRowCount(self.tw_reportTable.rowCount() + 2)

            self.write(lastRow, 0, "Сумма:")  # ! ????
            self.tw_reportTable.item(lastRow, 0).setBackground(QtGui.QColor(187, 255, 169))

            for i in range(10):
                if i != 0:
                    self.tw_reportTable.setItem(lastRow, i, QTableWidgetItem())
                    self.tw_reportTable.item(lastRow, i).setBackground(QtGui.QColor(187, 255, 169))

    def setTable(self):
        def color(row, column, red, green, blue):
            cell = self.tw_reportTable.item(row, column)
            cell.setBackground(QtGui.QColor(red, green, blue))

        self.tw_reportTable.verticalHeader().setVisible(False)
        self.tw_reportTable.horizontalHeader().setVisible(False)
        self.tw_reportTable.setColumnCount(10)
        self.tw_reportTable.setRowCount(2)

        for i in range(4):
            self.tw_reportTable.setSpan(0, i, 2, 1)
        self.tw_reportTable.setSpan(0, 4, 1, 6)

        names = ('Период аренды', 'Кол-во суток', 'Стоимость',
                 'Сумма', 'Оплата', 'Бронь', 'Гость', 'Авито', 'Расход',
                 'Показания', 'Доход')

        row = 0
        column = 0
        i = 0

        while column < 10:
            if column == 4:
                self.write(row, column, names[i])
                self.write(row + 1, column, names[i + 1])
                self.color(row, column)
                self.color(row + 1, column)
                row = 1
                i += 1
            else:
                self.write(row, column, names[i])
                self.color(row, column)

            column += 1
            i += 1

        horHeader = self.tw_reportTable.horizontalHeader()
        for i in range(self.tw_reportTable.columnCount()):
            horHeader.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def resizeable(self):
        verLayout = QVBoxLayout()
        horLayout = QHBoxLayout()

        lowRowItems = [self.btn_export, self.btn_save]

        for item in lowRowItems:
            horLayout.addWidget(item)

            if item == self.f_msg:
                item.setMinimumSize(QSize(300, 40))
            else:
                item.setMinimumSize(QSize(130, 30))

        horLayout.insertStretch(1, 130)
        verLayout.addWidget(self.tw_reportTable)
        sizePolicy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tw_reportTable.setSizePolicy(sizePolicy)
        verLayout.addLayout(horLayout)
        self.centralwidget.setLayout(verLayout)

    def resizeEvent(self, event):
        self.resized.emit()
        return self.resizeEvent(event)

    def frameReposition(self):
        height = self.frameSize().height()
        width = self.frameSize().width()
        width = int(width / 2 - 150)
        self.f_msg.move(QPoint(width, height + 200))
        self.animations.setScreenSize(width, height)
