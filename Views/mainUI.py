from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QtGui.QIcon('assets/icon96px.ico'))
        MainWindow.setWindowTitle("Hotel Journal")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.tb_main = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tb_main.setGeometry(QtCore.QRect(9, -1, 781, 541))
        self.tb_main.setObjectName("tb_main")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.m_file = QtWidgets.QMenu(parent=self.menubar)
        self.m_file.setObjectName("m_file")
        self.m_settings = QtWidgets.QMenu(parent=self.menubar)
        self.m_settings.setObjectName("m_settings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("ver 2.0")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.m_file.menuAction())
        self.menubar.addAction(self.m_settings.menuAction())

        self.retranslateUi(MainWindow)
        self.tb_main.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.m_file.setTitle(_translate("MainWindow", "File"))
        self.m_settings.setTitle(_translate("MainWindow", "Settings"))
