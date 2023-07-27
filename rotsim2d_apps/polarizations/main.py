from typing import List

import numpy as np
import PyQt5
import rotsim2d.dressedleaf as dl
import rotsim2d.pathways as pw
import rotsim2d.symbolic.functions as sym
import rotsim2d.symbolic.results as symr
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
import pyqtgraph as pg

from .AngleWidget import Ui_AngleWidget
from .PolarizationsUI import Ui_MainWindow
from .PolarizationWidget import PolarizationClassesWidget


class Model:
    ANGLES_SIZE = 250

    def __init__(self):
        self.rfactors = {int(k): sym.RFactor(v, 'experimental')
                         for v, k in symr.theta_labels.items()}
        self.angles = np.linspace(-np.pi/2, np.pi/2, self.ANGLES_SIZE)
        self.axes_labels = (r'&Phi;<sub>2</sub>', r'&Phi;<sub>3</sub>',
                            r'&Phi;<sub>4</sub>')

    def data_for_plots(self, angle_index: int, angle: float) -> List[np.ndarray]:
        args = [0, self.angles[:, None], self.angles[None, :]]
        args.insert(angle_index, angle*np.pi/180.0)

        return [self.rfactors[i+1].numeric_rel(*args)
                for i in range(len(self.rfactors))]

    def axes_labels_for_plot(self, angle_index: int) -> List[str]:
        labels = list(self.axes_labels)
        del labels[angle_index]

        return labels


class AngleWidget(QtWidgets.QWidget, Ui_AngleWidget):
    def __init__(self, label, enabled=False, parent=None):
        super(AngleWidget, self).__init__(parent)
        self.setupUi(self)
        self.label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label.setText(label)
        self.slider.valueChanged.connect(self.spin.setValue)
        self.spin.valueChanged.connect(self.slider.setValue)
        self.radio.toggled.connect(self.slider.setEnabled)
        self.radio.toggled.connect(self.spin.setEnabled)
        self.radio.setChecked(enabled)

class DocLabel(QtWidgets.QLabel):
    def __init__(self, ref_widget: QtWidgets.QWidget):
        super(DocLabel, self).__init__("Select one of the angles above to fix it at a specific value.<br><br>Polarization dependence as a function of remaining angles for each polarization class is shown on the right.<br><br>&Phi;<sub>1</sub> is fixed at 0&#176;.<br><br>The scale of &Theta;<sub>7</sub> class goes from -2 to +2.")
        self.setWordWrap(True)
        self.ref_widget = ref_widget

    def sizeHint(self) -> QtCore.QSize:
        super_hint = super().sizeHint()
        old_width = super_hint.width()
        super_hint.setWidth(self.ref_widget.sizeHint().width())
        super_hint.setHeight(round(super_hint.height()*\
                                   old_width/super_hint.width()))

        return super_hint


class Polarizations(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # take a reasonable amount of screen size
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        self.resize(int(screen.width()*0.7), int(screen.height()*0.7))

        # add angle widgets
        self._radio_group = QtWidgets.QButtonGroup()
        self._radio_group.buttonToggled.connect(
            self._radio_toggled)
        self._angle_widgets = []
        self.ui.anglesLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._add_angle_widget(AngleWidget("Φ<sub>2</sub>", True))
        self._add_angle_widget(AngleWidget("Φ<sub>3</sub>"))
        self._add_angle_widget(AngleWidget("Φ<sub>4</sub>"))
        self.ui.anglesLayout.setSpacing(10)

        label1 = DocLabel(self._angle_widgets[0])
        self.ui.anglesLayout.addWidget(label1)

        # add polarization widget
        self.classes_widget = PolarizationClassesWidget(
            Model.ANGLES_SIZE, self.ui.centralwidget)
        self.ui.centrallayout.addWidget(self.classes_widget)

        # add model
        self.ui.statusbar.showMessage("Initializing model")
        self.model = Model()
        self.update_plots()
        self.ui.statusbar.clearMessage()

    def _angle_index(self):
        index = 1
        for i in range(len(self._angle_widgets)):
            if self._angle_widgets[i].radio.isChecked():
                index += i

        return index

    def update_plots(self, val=None):
        index = self._angle_index()
        if val is None:
            val = self._angle_widgets[index-1].spin.value()
        self.classes_widget.figure_update(
            self.model.data_for_plots(index, val),
            self.model.axes_labels_for_plot(index-1))

    def _radio_toggled(self, button, checked):
        self.update_plots()

    def _add_angle_widget(self, wdg):
        wdg.spin.valueChanged.connect(self.update_plots)
        self._angle_widgets.append(wdg)
        self.ui.anglesLayout.addWidget(wdg)
        self._radio_group.addButton(wdg.radio)

def run():
    app = pg.mkQApp("Polarizations explorer")
    polarizations = Polarizations()
    polarizations.show()
    pg.exec()

# Local Variables:
# compile-comand: "make -k"
# End:
