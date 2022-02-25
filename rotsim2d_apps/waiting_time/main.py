import io
import itertools as it
import sys
from functools import partialmethod

import matplotlib as mpl
import numpy as np
import rotsim2d.dressedleaf as dl
import rotsim2d.pathways as pw
import rotsim2d.propagate as prop
import rotsim2d.symbolic.functions as sym
import rotsim2d.visual.functions as vis
from rotsim2d.rcpeaks import TBs, nth, RCPeaks
import scipy.constants as C
from molspecutils.molecule import CH3ClAlchemyMode, COAlchemyMode
from PyQt5 import QtCore, QtWidgets

from .Ui_WaitingTimeWindow import Ui_WaitingTimeWindow

nature_fontsize = 10
nature_rc = {
    # 'font.sans-serif': 'Arial',
    'font.size': nature_fontsize,
    'axes.labelsize': nature_fontsize,
    'xtick.labelsize': nature_fontsize,
    'ytick.labelsize': nature_fontsize,
    'legend.fontsize': nature_fontsize,
    'lines.markersize': 1.0,
    'lines.linewidth': 1.0,
    'xtick.major.size': 3,
    'xtick.minor.size': 1.5,
    'xtick.major.pad': 4,
    'ytick.major.size': 3,
    'ytick.major.pad': 4
}
mpl.rcParams.update(nature_rc)


class DressedPathwaysModel(QtCore.QAbstractListModel):
    def __init__(self, rc_peaks: RCPeaks, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.rc_peaks = rc_peaks

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.rc_peaks)

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() >= self.rowCount():
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.rc_peaks.render(index.row())
        else:
            return None


class WaitingTimeWindow(QtWidgets.QMainWindow, Ui_WaitingTimeWindow):
    def __init__(self):
        super(WaitingTimeWindow, self).__init__()
        self.setupUi(self)

        self.plots_widget.update_plot_button.clicked.connect(
            self.handle_update_plot)
        # set up pathways widget
        self.setup_pathwayswidget()

        self.update_model()
        self.pws_widget.pw_list.setCurrentIndex(
            self.dpmodel.index(0, 0))
        self.pws_widget.pw_list.activated.emit(
            self.dpmodel.index(0, 0))

    def setup_pathwayswidget(self):
        self.pws_widget.j_spin.valueChanged.connect(
            self.pws_widget.k_spin.setMaximum)
        self.pws_widget.j_spin.valueChanged.emit(
            self.pws_widget.j_spin.value())
        self.pws_widget.pw_list.activated.connect(
            self.plot_rcs)
        self.pws_widget.pw_list.activated.connect(
            self.update_sec_axes)
        self.pws_widget.pw_list.activated.connect(
            self.print_diagrams)
        self.plot_print_button.clicked.connect(
            self.handle_plot_print)

        self.pws_widget.molecule_combo.addItems(["CO", "CH3Cl"])
        self.pws_widget.direction_combo.addItems(["SII", "SI"])
        self.pws_widget.update_model.clicked.connect(self.update_model)

    @QtCore.pyqtSlot()
    def handle_update_plot(self):
        index = self.pws_widget.pw_list.currentIndex()
        if index.isValid():
            self.plot_rcs(index)

    @QtCore.pyqtSlot()
    def handle_plot_print(self):
        index = self.pws_widget.pw_list.currentIndex()
        if index.isValid():
            self.plot_rcs(index)
            self.update_sec_axes(index)
            self.print_diagrams(index)

    @QtCore.pyqtSlot(bool)
    def update_model(self, checked=True):
        molecule = self.pws_widget.molecule_combo.currentText()
        direction = self.pws_widget.direction_combo.currentText()
        j = self.pws_widget.j_spin.value()
        k = self.pws_widget.k_spin.value()
        self.dpmodel = DressedPathwaysModel(RCPeaks(molecule, direction, j, k))
        self.pws_widget.pw_list.setModel(self.dpmodel)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def print_diagrams(self, index):
        buf = io.StringIO()
        def buf_print(s: str='', end='\n'):
            buf.write(s+end)
        pws = nth(iter(self.dpmodel.rc_peaks.dps), index.row())
        dl.pprint_dllist(pws, True, print=buf_print)
        self.diagrams.setPlainText(buf.getvalue())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def update_sec_axes(self, index):
        molecule = self.pws_widget.molecule_combo.currentText()
        TB = TBs[molecule]
        for ax in self.plots_widget.secaxes:
            ax.set_functions((
                lambda tb_frac: tb_frac*TB*1e12,
                lambda tw: tw/TB/1e12))

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def plot_rcs(self, index):
        pws = nth(iter(self.dpmodel.rc_peaks.dps), index.row())
        molecule = self.pws_widget.molecule_combo.currentText()
        j = self.pws_widget.j_spin.value()
        TB = TBs[molecule]
        xmin = self.plots_widget.xmin_spin.value()
        xmax = self.plots_widget.xmax_spin.value()
        tws = np.linspace(xmin*TB, xmax*TB, 5000)
        resp = np.zeros((len(pws), tws.size), dtype=np.complex128)
        for i in range(len(pws)):
            resp[i] = prop.dressed_leaf_response(
                pws[i], [None, tws, None],
                ['t', 't', 't'], p=1e-4)

        ax1 = self.plots_widget.axes[1]
        while ax1.lines:
            ax1.lines.remove(ax1.lines[0])
        ax1.set_prop_cycle(None)
        if self.plots_widget.real_radio.isChecked():
            ax1.plot(tws/TB, resp.real.sum(axis=0), label='real')
        else:
            ax1.plot(tws/TB, resp.imag.sum(axis=0), label='imaginary')
        ax1.legend(loc='lower right', bbox_to_anchor=[1.0, 1.1], ncol=2)

        ax0 = self.plots_widget.axes[0]
        while ax0.lines:
            ax0.lines.remove(ax0.lines[0])
        # ax0.relim()
        ax0.set_prop_cycle(None)
        for i in range(len(pws)):
            label = '$'+vis.latex(sym.rcs_expression(pws[i].coherences[1], j))+'$'
            if self.plots_widget.real_radio.isChecked():
                ax0.plot(tws/TB, resp[i].real, label=label)
            else:
                ax0.plot(tws/TB, resp[i].imag, label=label)
        ax0.legend(loc='lower right', bbox_to_anchor=[1.0, 1.1], ncol=2)

        ax1.relim()
        ax0.relim()
        if self.plots_widget.holdy_check.isChecked():
            ax1.autoscale(True, "x", True)
            ax0.autoscale(True, "x", True)
        else:
            ax1.autoscale(True, "both", True)
            ax0.autoscale(True, "both", True)

        self.plots_widget.mpl.canvas.draw()

def run():
    app = QtWidgets.QApplication(sys.argv)
    mpl.rcParams['figure.dpi'] = app.desktop().physicalDpiX()
    mw = WaitingTimeWindow()
    mw.show()
    sys.exit(app.exec_())
