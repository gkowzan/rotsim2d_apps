# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_PlotsWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlotsWidget(object):
    def setupUi(self, PlotsWidget):
        PlotsWidget.setObjectName("PlotsWidget")
        PlotsWidget.resize(701, 472)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PlotsWidget.sizePolicy().hasHeightForWidth())
        PlotsWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(PlotsWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mpl = MplWidget(PlotsWidget)
        self.mpl.setObjectName("mpl")
        self.verticalLayout.addWidget(self.mpl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.xlims_label = QtWidgets.QLabel(PlotsWidget)
        self.xlims_label.setObjectName("xlims_label")
        self.horizontalLayout.addWidget(self.xlims_label)
        self.xmin_spin = QtWidgets.QDoubleSpinBox(PlotsWidget)
        self.xmin_spin.setSingleStep(0.05)
        self.xmin_spin.setObjectName("xmin_spin")
        self.horizontalLayout.addWidget(self.xmin_spin)
        self.xmax_spin = QtWidgets.QDoubleSpinBox(PlotsWidget)
        self.xmax_spin.setSingleStep(0.05)
        self.xmax_spin.setProperty("value", 2.0)
        self.xmax_spin.setObjectName("xmax_spin")
        self.horizontalLayout.addWidget(self.xmax_spin)
        self.real_radio = QtWidgets.QRadioButton(PlotsWidget)
        self.real_radio.setChecked(True)
        self.real_radio.setObjectName("real_radio")
        self.horizontalLayout.addWidget(self.real_radio)
        self.imag_radio = QtWidgets.QRadioButton(PlotsWidget)
        self.imag_radio.setObjectName("imag_radio")
        self.horizontalLayout.addWidget(self.imag_radio)
        self.holdy_check = QtWidgets.QCheckBox(PlotsWidget)
        self.holdy_check.setObjectName("holdy_check")
        self.horizontalLayout.addWidget(self.holdy_check)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.update_plot_button = QtWidgets.QPushButton(PlotsWidget)
        self.update_plot_button.setObjectName("update_plot_button")
        self.horizontalLayout.addWidget(self.update_plot_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PlotsWidget)
        QtCore.QMetaObject.connectSlotsByName(PlotsWidget)

    def retranslateUi(self, PlotsWidget):
        _translate = QtCore.QCoreApplication.translate
        PlotsWidget.setWindowTitle(_translate("PlotsWidget", "Form"))
        self.xlims_label.setText(_translate("PlotsWidget", "X limits (1/B)"))
        self.real_radio.setText(_translate("PlotsWidget", "Real"))
        self.imag_radio.setText(_translate("PlotsWidget", "Imaginary"))
        self.holdy_check.setText(_translate("PlotsWidget", "Hold Y"))
        self.update_plot_button.setText(_translate("PlotsWidget", "Update plot"))
from .MplWidget import MplWidget
