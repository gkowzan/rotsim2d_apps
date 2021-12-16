from PyQt5 import QtWidgets, QtCore
from .Ui_PlotsWidget import Ui_PlotsWidget

class PlotsWidget(QtWidgets.QWidget, Ui_PlotsWidget):
    def __init__(self, parent=None):
        super(PlotsWidget, self).__init__(parent)
        self.setupUi(self)

        self.fig = self.mpl.canvas.fig
        self.gs = self.fig.add_gridspec(
            ncols=2, nrows=1, width_ratios=[1, 1])
        self.axes = [self.fig.add_subplot(self.gs[i]) for i in (0, 1)]
        self.secaxes = [ax.secondary_xaxis('top', functions=(
            lambda x: x, lambda x: x)) for ax in self.axes]
        self.axes[0].set_title('Individual', loc='left')
        self.axes[1].set_title("Sum", loc='left')
        for ax in self.axes:
            ax.set(xlabel='Time (1/B)', ylabel='Amplitude')
            ax.margins(0.0)
            ax.autoscale(True, 'both', True)
        for ax in self.secaxes:
            ax.set_xlabel('Time (ps)')
        self.fig.set_constrained_layout_pads(
            wspace=0.02, hspace=0.02)

        self.holdy_check.setChecked(False)
        self.holdy_check.stateChanged.connect(self.handle_holdy)

    @QtCore.pyqtSlot(int)
    def handle_holdy(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            for ax in self.axes:
                ax.autoscale(False, 'y', None)
                ax.autoscale(True, 'x', None)
        elif state == QtCore.Qt.CheckState.Unchecked:
            for ax in self.axes:
                ax.autoscale(True, 'both', None)
