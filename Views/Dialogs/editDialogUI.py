from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(370, 430)

        self.btn_save = QtWidgets.QPushButton(parent=Dialog)
        self.btn_save.setGeometry(QtCore.QRect(240, 170, 121, 23))
        self.btn_save.setObjectName("btn_save")

        self.te_notes = QtWidgets.QTextEdit(parent=Dialog)
        self.te_notes.setGeometry(QtCore.QRect(10, 200, 351, 221))
        self.te_notes.setCursorWidth(1)
        self.te_notes.setObjectName("te_notes")

        self.date_out = QtWidgets.QDateEdit(parent=Dialog)
        self.date_out.setGeometry(QtCore.QRect(10, 140, 71, 22))
        self.date_out.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_out.setObjectName("date_out")

        self.lbl_name = QtWidgets.QLabel(parent=Dialog)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")

        self.btn_color = QtWidgets.QPushButton(parent=Dialog)
        self.btn_color.setGeometry(QtCore.QRect(10, 170, 121, 23))
        self.btn_color.setObjectName("btn_color")

        self.lbl_dateIn = QtWidgets.QLabel(parent=Dialog)
        self.lbl_dateIn.setGeometry(QtCore.QRect(10, 60, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_dateIn.setFont(font)
        self.lbl_dateIn.setObjectName("lbl_dateIn")

        self.lbl_timeIn = QtWidgets.QLabel(parent=Dialog)
        self.lbl_timeIn.setGeometry(QtCore.QRect(150, 60, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_timeIn.setFont(font)
        self.lbl_timeIn.setObjectName("lbl_timeIn")

        self.time_in = QtWidgets.QTimeEdit(parent=Dialog)
        self.time_in.setGeometry(QtCore.QRect(150, 80, 71, 22))
        self.time_in.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_in.setObjectName("time_in")

        self.date_in = QtWidgets.QDateEdit(parent=Dialog)
        self.date_in.setGeometry(QtCore.QRect(10, 80, 71, 22))
        self.date_in.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_in.setObjectName("date_in")

        self.lbl_dateOut = QtWidgets.QLabel(parent=Dialog)
        self.lbl_dateOut.setGeometry(QtCore.QRect(10, 120, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_dateOut.setFont(font)
        self.lbl_dateOut.setObjectName("lbl_dateOut")

        self.lbl_timeOut = QtWidgets.QLabel(parent=Dialog)
        self.lbl_timeOut.setGeometry(QtCore.QRect(150, 120, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_timeOut.setFont(font)
        self.lbl_timeOut.setObjectName("lbl_timeOut")

        self.time_out = QtWidgets.QTimeEdit(parent=Dialog)
        self.time_out.setGeometry(QtCore.QRect(150, 140, 71, 22))
        self.time_out.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_out.setObjectName("time_out")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_save.setText(_translate("Dialog", "сохранить"))
        self.te_notes.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.te_notes.setPlaceholderText(_translate("Dialog", "заметки"))
        self.date_out.setDisplayFormat(_translate("Dialog", "dd.MM"))
        self.lbl_name.setText(_translate("Dialog", "Внесение записи"))
        self.btn_color.setText(_translate("Dialog", "выбрать цвет "))
        self.lbl_dateIn.setText(_translate("Dialog", "дата заезда"))
        self.lbl_timeIn.setText(_translate("Dialog", "время заезда"))
        self.date_in.setDisplayFormat(_translate("Dialog", "dd.MM"))
        self.lbl_dateOut.setText(_translate("Dialog", "дата выезда"))
        self.lbl_timeOut.setText(_translate("Dialog", "время выезда"))
