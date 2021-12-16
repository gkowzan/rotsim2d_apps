# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_PathwaysWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PathwaysWidget(object):
    def setupUi(self, PathwaysWidget):
        PathwaysWidget.setObjectName("PathwaysWidget")
        PathwaysWidget.resize(326, 390)
        self.verticalLayout = QtWidgets.QVBoxLayout(PathwaysWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 9, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.molecule_combo = QtWidgets.QComboBox(PathwaysWidget)
        self.molecule_combo.setCurrentText("")
        self.molecule_combo.setObjectName("molecule_combo")
        self.gridLayout.addWidget(self.molecule_combo, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(PathwaysWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(PathwaysWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.j_spin = QtWidgets.QSpinBox(PathwaysWidget)
        self.j_spin.setProperty("value", 10)
        self.j_spin.setObjectName("j_spin")
        self.gridLayout.addWidget(self.j_spin, 2, 1, 1, 1)
        self.update_model = QtWidgets.QPushButton(PathwaysWidget)
        self.update_model.setObjectName("update_model")
        self.gridLayout.addWidget(self.update_model, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(PathwaysWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.k_spin = QtWidgets.QSpinBox(PathwaysWidget)
        self.k_spin.setProperty("value", 1)
        self.k_spin.setObjectName("k_spin")
        self.gridLayout.addWidget(self.k_spin, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(PathwaysWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.direction_combo = QtWidgets.QComboBox(PathwaysWidget)
        self.direction_combo.setObjectName("direction_combo")
        self.gridLayout.addWidget(self.direction_combo, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_5 = QtWidgets.QLabel(PathwaysWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.pw_list = ListView(PathwaysWidget)
        self.pw_list.setObjectName("pw_list")
        self.verticalLayout.addWidget(self.pw_list)

        self.retranslateUi(PathwaysWidget)
        self.molecule_combo.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(PathwaysWidget)

    def retranslateUi(self, PathwaysWidget):
        _translate = QtCore.QCoreApplication.translate
        PathwaysWidget.setWindowTitle(_translate("PathwaysWidget", "Form"))
        self.label_3.setText(_translate("PathwaysWidget", "K"))
        self.label_2.setText(_translate("PathwaysWidget", "J"))
        self.update_model.setText(_translate("PathwaysWidget", "Update list"))
        self.label.setText(_translate("PathwaysWidget", "Molecule"))
        self.label_4.setText(_translate("PathwaysWidget", "Direction"))
        self.label_5.setText(_translate("PathwaysWidget", "Rotationally coherent peaks/pathways:"))
from .ListView import ListView
