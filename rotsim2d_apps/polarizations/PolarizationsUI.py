# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PolarizationsUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 661)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centrallayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centrallayout.setObjectName("centrallayout")
        self.anglesLayout = QtWidgets.QVBoxLayout()
        self.anglesLayout.setObjectName("anglesLayout")
        self.centrallayout.addLayout(self.anglesLayout)
        self.mplwdg = PolarizationWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwdg.sizePolicy().hasHeightForWidth())
        self.mplwdg.setSizePolicy(sizePolicy)
        self.mplwdg.setMinimumSize(QtCore.QSize(200, 0))
        self.mplwdg.setObjectName("mplwdg")
        self.centrallayout.addWidget(self.mplwdg)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Polarization explorer"))
from .PolarizationWidget import PolarizationWidget
