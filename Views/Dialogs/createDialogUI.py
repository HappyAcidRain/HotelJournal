from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(353, 110)

        self.btn_create = QtWidgets.QPushButton(parent=Dialog)
        self.btn_create.setGeometry(QtCore.QRect(260, 80, 75, 23))
        self.btn_create.setObjectName("btn_create")

        self.le_name = QtWidgets.QLineEdit(parent=Dialog)
        self.le_name.setGeometry(QtCore.QRect(40, 50, 271, 21))
        self.le_name.setObjectName("le_name")

        self.lbl_name = QtWidgets.QLabel(parent=Dialog)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 331, 31))
        self.lbl_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setObjectName("lbl_name")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_create.setText(_translate("Dialog", "создать"))
        self.lbl_name.setText(_translate("Dialog", "Введите имя новой таблицы"))
