from PyQt5 import QtWidgets
from .Ui_PathwaysWidget import Ui_PathwaysWidget

class PathwaysWidget(QtWidgets.QWidget, Ui_PathwaysWidget):
    def __init__(self, parent=None):
        super(PathwaysWidget, self).__init__(parent)
        self.setupUi(self)
