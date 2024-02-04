from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(297, 170)
        font = QtGui.QFont()
        font.setPointSize(11)
        
        self.date_out = QtWidgets.QDateEdit(parent=Dialog)
        self.date_out.setGeometry(QtCore.QRect(160, 80, 71, 22))
        self.date_out.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_out.setObjectName("date_out")
        
        self.date_in = QtWidgets.QDateEdit(parent=Dialog)
        self.date_in.setGeometry(QtCore.QRect(50, 80, 71, 22))
        self.date_in.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_in.setObjectName("date_in")
        
        self.lbl_dateOut = QtWidgets.QLabel(parent=Dialog)
        self.lbl_dateOut.setGeometry(QtCore.QRect(160, 60, 71, 16))
        self.lbl_dateOut.setFont(font)
        self.lbl_dateOut.setObjectName("lbl_dateOut")
        
        self.lbl_dateIn = QtWidgets.QLabel(parent=Dialog)
        self.lbl_dateIn.setGeometry(QtCore.QRect(50, 60, 111, 16))
        self.lbl_dateIn.setFont(font)
        self.lbl_dateIn.setObjectName("lbl_dateIn")
        
        self.lbl_name = QtWidgets.QLabel(parent=Dialog)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font.setPointSize(18)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")
        
        self.btn_del = QtWidgets.QPushButton(parent=Dialog)
        self.btn_del.setGeometry(QtCore.QRect(180, 130, 113, 32))
        self.btn_del.setObjectName("btn_del")
        
        self.btn_cancel = QtWidgets.QPushButton(parent=Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(10, 130, 113, 32))
        self.btn_cancel.setObjectName("btn_cancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.date_out.setDisplayFormat(_translate("Dialog", "dd.MM"))
        self.date_in.setDisplayFormat(_translate("Dialog", "dd.MM"))
        self.lbl_dateOut.setText(_translate("Dialog", "дата выезда"))
        self.lbl_dateIn.setText(_translate("Dialog", "дата заезда"))
        self.lbl_name.setText(_translate("Dialog", "Удаление записи"))
        self.btn_del.setText(_translate("Dialog", "удалить"))
        self.btn_cancel.setText(_translate("Dialog", "закрыть"))
