import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from .PolarizationsUI import Ui_MainWindow
from .AngleWidget import Ui_AngleWidget
import matplotlib as mpl
import numpy as np
import rotsim2d.pathways as pw
import rotsim2d.dressedleaf as dl
import rotsim2d.symbolic.functions as sym


class Model:
    def __init__(self):
        kbs = pw.gen_pathways([5], rotor='symmetric', meths=[pw.only_SII],
                              kiter_func=lambda x: [1],
                              pump_overlap=False)
        pws = dl.Pathway.from_kb_list(kbs)
        rf_pws = sym.RFactorPathways.from_pwlist(pws, True, True)
        self.rfactors = [rfpw.rfactor for rfpw in rf_pws]
        self.titles = ['peaks: '+','.join(rfpw.peak_labels)+'\n'+
                       'trans: '+','.join(rfpw.trans_labels_deg)
                       for rfpw in rf_pws]
        self.angles = np.linspace(-np.pi/2, np.pi/2, 100)
        self.axes_labels = (r'$\Phi_2$', r'$\Phi_3$', r'$\Phi_4$')

    def plot_data(self, index, val):
        args = [0, self.angles[:, None], self.angles[None, :]]
        args.insert(index, val*np.pi/180.0)
        data = [rfactor.numeric_rel(*args) for rfactor in self.rfactors]

        return data

    def plot_axes_labels(self, index):
        labels = list(self.axes_labels)
        del labels[index]
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


class Polarizations(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # take a reasonable amount of screen size
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        self.resize(screen.width()*0.7, screen.height()*0.7)

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

        # add model
        self.ui.statusbar.showMessage("Initializing model")
        self.model = Model()
        self.ui.mplwdg.set_titles(self.model.titles)
        # self.update_plots()
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
        data = self.model.plot_data(index, val)
        self.ui.mplwdg.figure_update(data)

    def update_axes_labels(self):
        index = self._angle_index()
        labels = self.model.plot_axes_labels(index-1)
        self.ui.mplwdg.set_axes_labels(labels)

    def _radio_toggled(self, button, checked):
        self.update_plots()
        self.update_axes_labels()

    def _add_angle_widget(self, wdg):
        wdg.spin.valueChanged.connect(self.update_plots)
        self._angle_widgets.append(wdg)
        self.ui.anglesLayout.addWidget(wdg)
        self._radio_group.addButton(wdg.radio)

def run():
    app = QtWidgets.QApplication(sys.argv)
    mpl.rcParams['figure.dpi'] = app.desktop().physicalDpiX()
    polarizations = Polarizations()
    polarizations.show()
    sys.exit(app.exec_())

# Local Variables:
# compile-comand: "make -k"
# End:
