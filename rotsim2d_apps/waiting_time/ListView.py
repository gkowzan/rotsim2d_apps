from PyQt5 import QtWidgets, QtCore

class ListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        # self.setSizePolicy(
        #     QtWidgets.QSizePolicy.Policy.Maximum,
        #     self.sizePolicy().verticalPolicy())

    def sizeHint(self):
        return QtCore.QSize(
            self.sizeHintForColumn(0)+25,
            super(ListView, self).sizeHint().height())
