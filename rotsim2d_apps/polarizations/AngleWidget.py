# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AngleWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AngleWidget(object):
    def setupUi(self, AngleWidget):
        AngleWidget.setObjectName("AngleWidget")
        AngleWidget.resize(342, 70)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AngleWidget.sizePolicy().hasHeightForWidth())
        AngleWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(AngleWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.spin = QtWidgets.QDoubleSpinBox(AngleWidget)
        self.spin.setEnabled(False)
        self.spin.setSuffix("°")
        self.spin.setMinimum(-90.0)
        self.spin.setMaximum(90.0)
        self.spin.setObjectName("spin")
        self.gridLayout.addWidget(self.spin, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(AngleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.radio = QtWidgets.QRadioButton(AngleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radio.sizePolicy().hasHeightForWidth())
        self.radio.setSizePolicy(sizePolicy)
        self.radio.setText("")
        self.radio.setObjectName("radio")
        self.gridLayout.addWidget(self.radio, 0, 0, 1, 1)
        self.slider = QtWidgets.QSlider(AngleWidget)
        self.slider.setEnabled(False)
        self.slider.setMinimum(-90)
        self.slider.setMaximum(90)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setObjectName("slider")
        self.gridLayout.addWidget(self.slider, 1, 0, 1, 3)

        self.retranslateUi(AngleWidget)
        QtCore.QMetaObject.connectSlotsByName(AngleWidget)

    def retranslateUi(self, AngleWidget):
        _translate = QtCore.QCoreApplication.translate
        AngleWidget.setWindowTitle(_translate("AngleWidget", "Form"))
        self.label.setText(_translate("AngleWidget", "TextLabel"))
