from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 84)

        self.pb_save = QtWidgets.QProgressBar(parent=Dialog)
        self.pb_save.setGeometry(QtCore.QRect(10, 50, 381, 21))
        self.pb_save.setProperty("value", 24)
        self.pb_save.setObjectName("pb_save")

        self.lbl_saveText = QtWidgets.QLabel(parent=Dialog)
        self.lbl_saveText.setGeometry(QtCore.QRect(10, 9, 381, 31))
        self.lbl_saveText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_saveText.setObjectName("lbl_saveText")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_saveText.setText(_translate("Dialog", "Идёт сохранение..."))
