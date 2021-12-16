# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_WaitingTimeWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WaitingTimeWindow(object):
    def setupUi(self, WaitingTimeWindow):
        WaitingTimeWindow.setObjectName("WaitingTimeWindow")
        WaitingTimeWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(WaitingTimeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pws_widget = PathwaysWidget(self.tab)
        self.pws_widget.setObjectName("pws_widget")
        self.horizontalLayout_2.addWidget(self.pws_widget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.diagrams = QtWidgets.QTextEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self.diagrams.setFont(font)
        self.diagrams.setReadOnly(True)
        self.diagrams.setAcceptRichText(False)
        self.diagrams.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.diagrams.setObjectName("diagrams")
        self.horizontalLayout_3.addWidget(self.diagrams)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.plot_print_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_print_button.setObjectName("plot_print_button")
        self.verticalLayout.addWidget(self.plot_print_button)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.plots_widget = PlotsWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plots_widget.sizePolicy().hasHeightForWidth())
        self.plots_widget.setSizePolicy(sizePolicy)
        self.plots_widget.setObjectName("plots_widget")
        self.horizontalLayout.addWidget(self.plots_widget)
        WaitingTimeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WaitingTimeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        WaitingTimeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WaitingTimeWindow)
        self.statusbar.setObjectName("statusbar")
        WaitingTimeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(WaitingTimeWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WaitingTimeWindow)

    def retranslateUi(self, WaitingTimeWindow):
        _translate = QtCore.QCoreApplication.translate
        WaitingTimeWindow.setWindowTitle(_translate("WaitingTimeWindow", "Waiting time"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("WaitingTimeWindow", "Pathways"))
        self.diagrams.setHtml(_translate("WaitingTimeWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Monospace\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'monospace\';\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("WaitingTimeWindow", "Diagrams"))
        self.plot_print_button.setText(_translate("WaitingTimeWindow", "Plot coherences/print diagrams"))
from .PathwaysWidget import PathwaysWidget
from .PlotsWidget import PlotsWidget
