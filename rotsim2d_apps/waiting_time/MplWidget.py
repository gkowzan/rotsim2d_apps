from PyQt5 import QtWidgets
from ..MplCanvas import MplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, parent)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
