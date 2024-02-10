from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView

from ViewModel.Dialogs import saveDialog
from ViewModel.Threads import sumTableThread

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

        self.totalList = []
        self.reportSum = sumTableThread.SumReportThread()
        self.reportSum.s_sumData.connect(self.change_sum_row)

        self.saveDialog = saveDialog.SaveDialog()

        self.reportSum = sumTableThread.SumReportThread()
        self.reportSum.s_sumData.connect(self.change_sum_row)

        self.saveDialog = saveDialog.SaveDialog()

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tw_reportTable = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tw_reportTable.setGeometry(QtCore.QRect(0, 0, 1011, 451))

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.tw_reportTable.sizePolicy().hasHeightForWidth())

        self.tw_reportTable.setSizePolicy(size_policy)
        self.tw_reportTable.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tw_reportTable.setObjectName("tw_reportTable")
        self.tw_reportTable.setColumnCount(0)
        self.tw_reportTable.setRowCount(0)
        self.tw_reportTable.cellChanged.connect(self.calculate)

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

        self.set_table()

    def set_sum_row(self):
        if self.tw_reportTable.item(self.tw_reportTable.rowCount() - 1, 0) is not None:

            last_row = self.tw_reportTable.rowCount() + 1
            self.tw_reportTable.setRowCount(self.tw_reportTable.rowCount() + 2)

            self.write(last_row, 0, "Сумма:")
            self.tw_reportTable.item(last_row, 0).setBackground(QtGui.QColor(187, 255, 169))

            for i in range(10):
                if i != 0:
                    self.tw_reportTable.setItem(last_row, i, QTableWidgetItem())
                    self.tw_reportTable.item(last_row, i).setBackground(QtGui.QColor(187, 255, 169))

    def calculate(self, row, column):
        if column == 2:
            entered = self.tw_reportTable.currentItem()
            if entered and entered.text().isdigit():
                days = self.tw_reportTable.item(row, 1).text()
                self.write(row, 3, str(int(entered.text()) * int(days)))

        elif column == 4 or 5 or 6 or 9:
            self.reportSum.set(self.tw_reportTable)
            self.reportSum.start()

    def change_sum_row(self, total):
        last_row = self.tw_reportTable.rowCount() - 1
        alignment = QtCore.Qt.AlignmentFlag.AlignCenter
        self.totalList.append(total)

        if len(self.totalList) == 4:
            column = 4
            for item in self.totalList:
                cell = self.tw_reportTable.item(last_row, column)
                if cell is None:
                    return

                cell.setText(str(item))
                cell.setTextAlignment(alignment)
                if column < 6:
                    column += 1
                else:
                    column = 9

            self.totalList.clear()

    def save_dialog(self, msg):
        if msg == 'upd':
            self.saveDialog.add()
        else:
            self.saveDialog.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_save.setText(_translate("MainWindow", "Сохранить"))
        self.btn_export.setText(_translate("MainWindow", "Экспорт"))
        self.lbl_msg.setText(_translate("MainWindow", "Таблица экспортирована!"))

    def set_table(self):
        self.tw_reportTable.verticalHeader().setVisible(False)
        self.tw_reportTable.horizontalHeader().setVisible(False)
        self.tw_reportTable.setColumnCount(10)
        self.tw_reportTable.setRowCount(2)

        for i in range(4):
            self.tw_reportTable.setSpan(0, i, 2, 1)
        self.tw_reportTable.setSpan(0, 4, 1, 6)
        names = ('Период аренды', 'Кол-во суток', 'Стоимость',
                 'Сумма', 'Оплата', 'Бронь', 'Гость', 'Авито',
                 'Расход','Показания', 'Доход')

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

        hor_header = self.tw_reportTable.horizontalHeader()
        for i in range(self.tw_reportTable.columnCount()):
            hor_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def write(self, row, column, text):
        alignment = QtCore.Qt.AlignmentFlag.AlignCenter
        self.tw_reportTable.setItem(row, column, QTableWidgetItem())
        self.tw_reportTable.item(row, column).setText(text)
        self.tw_reportTable.item(row, column).setTextAlignment(alignment)
        self.color(row, column)

    def color(self, row, column):

        colors = ((191, 255, 172), (255, 219, 224), (249, 211, 249),
                  (249, 211, 249), (243, 243, 155), (255, 237, 178),
                  (202, 199, 248))

        match column:

            case 4:
                if row == 0:
                    red, green, blue = colors[0]
                    cell = self.tw_reportTable.item(row, column)
                    cell.setBackground(QtGui.QColor(red, green, blue))

                else:
                    red, green, blue = colors[1]
                    cell = self.tw_reportTable.item(row, column)
                    cell.setBackground(QtGui.QColor(red, green, blue))

            case 5:
                red, green, blue = colors[2]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 6:
                red, green, blue = colors[3]
                cell = self.tw_reportTable.item(row, column)

                cell.setBackground(QtGui.QColor(red, green, blue))

            case 7:
                red, green, blue = colors[4]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 8:
                red, green, blue = colors[5]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

            case 9:
                red, green, blue = colors[6]
                cell = self.tw_reportTable.item(row, column)
                cell.setBackground(QtGui.QColor(red, green, blue))

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
