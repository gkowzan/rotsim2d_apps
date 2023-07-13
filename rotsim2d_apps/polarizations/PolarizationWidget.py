from typing import Sequence
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

pg.setConfigOptions(
    antialias=True,
    imageAxisOrder='row-major')


class PolarizationClassItem(pg.PlotItem):
    "Extends PlotItem and contains ImageItem."
    def __init__(self, angles_size: int, title: str):
        pg.PlotItem.__init__(self)
        self.image_item = pg.ImageItem(np.zeros((angles_size, angles_size)),
                                       autoLevels=False,
                                       # axisOrder='row-major',
                                       levels=(-1.0, 1.0))
        # self.image_item.setColorMap("CET-D1A")
        self.image_item.setColorMap(pg.colormap.get('bwr', source='matplotlib'))
        tr = QtGui.QTransform()
        tr.scale(180.0/angles_size, 180.0/angles_size)
        tr.translate(-angles_size/2, -angles_size/2)
        self.image_item.setTransform(tr)

        self.setDefaultPadding(0.0)
        self.setMouseEnabled(x=False, y=False)
        self.setAspectLocked()
        self.addItem(self.image_item)
        self.disableAutoRange()
        self.setTitle(title)
        self.setLabel('bottom', r'&Phi;<sub>3</sub>', units='&#176;')
        self.setLabel('left', r'&Phi;<sub>4</sub>', units='&#176;')

        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.addItem(self.vline, ignoreBounds=True)
        self.addItem(self.hline, ignoreBounds=True)

    def update(self, data: np.ndarray, labels: Sequence[str]):
        self.image_item.setImage(data, levels=(-1.0, 1.0))
        self.setLabel('bottom', labels[0], units='&#176;')
        self.setLabel('left', labels[1], units='&#176;')

    def mouse_moved(self, ev):
        if self.sceneBoundingRect().contains(ev):
            mouse_point = self.vb.mapSceneToView(ev)
            self.vline.setPos(mouse_point.x())
            self.hline.setPos(mouse_point.y())

class CrosshairManager:
    @staticmethod
    def coerce(val, min, max):
        if val < min:
            return min
        if val > max:
            return max
        return val

    def __init__(self, pcw: 'PolarizationClassesWidget'):
        self.pcw = pcw
        self.lines = []
        for pi in pcw.polarization_items:
            self.lines.append((pi.vline, pi.hline))

    def mouse_moved(self, ev):
        in_plots = [pi.sceneBoundingRect().contains(ev)
                    for pi in self.pcw.polarization_items]
        if not any(in_plots):
            for line in self.lines:
                line[0].setVisible(False)
                line[1].setVisible(False)
        else:
            index = in_plots.index(True)
            pi = self.pcw.polarization_items[index]
            mouse_point = pi.vb.mapSceneToView(ev)
            x, y = mouse_point.x(), mouse_point.y()
            index_point = pi.vb.mapFromViewToItem(pi.image_item, mouse_point)
            max = pi.image_item.image.shape[0]
            ix = self.coerce(int(index_point.x()), 0, max-1)
            iy = self.coerce(int(index_point.y()), 0, max-1)
            for line in self.lines:
                line[0].setPos(x)
                line[1].setPos(y)
                line[0].setVisible(True)
                line[1].setVisible(True)
            self.pcw.data_label.setText(
                "{:s}={:.2f}&#176;, {:s}={:.2f}&#176;, z={:.4f}".format(
                    self.pcw.axes_labels[0], x, self.pcw.axes_labels[1], y,
                    pi.image_item.image[ix, iy]
                ))
            self.pcw.data_label.setVisible(True)


class PolarizationClassesWidget(pg.GraphicsLayoutWidget):
    "Extends GraphicsLayoutWidget."
    def __init__(self, angles_size: int, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent=parent, show=True)

        self.addLabel('<span style="font-size: 20pt;">'
                      'R(0&#176;, &Phi;<sub>2</sub>,'
                      ' &Phi;<sub>3</sub>, &Phi;<sub>4</sub>)/'
                      'R(0&#176;, 0&#176;, 0&#176;, 0&#176;)'
                      '</span>',
                      colspan=5,
                      justify='center')
        self.nextRow()
        self.data_label = pg.LabelItem(justify='left')
        self.addItem(self.data_label, colspan=5)
        self.cbar = pg.ColorBarItem(
            width=25,
            interactive=False)
        self.addItem(self.cbar, 2, 4, 2, 1)
        self.nextRow()
        self.polarization_items = []
        for i in range(1, 4):
            self.polarization_items.append(
                PolarizationClassItem(
                    angles_size,
                    r'<span style="font-weight:bold; font-size:14pt;">&Theta;<sub>{:d}</sub></span>'.format(i)))
            self.addItem(self.polarization_items[-1])
        self.nextRow()
        for i in range(4, 8):
            self.polarization_items.append(
                PolarizationClassItem(
                    angles_size,
                    r'<span style="font-weight:bold; font-size:14pt;">&Theta;<sub>{:d}</sub></span>'.format(i)))
            self.addItem(self.polarization_items[-1])
        self.cbar.setImageItem([pi.image_item for pi in self.polarization_items])

        self.xhair_mgr = CrosshairManager(self)
        self.scene().sigMouseMoved.connect(self.xhair_mgr.mouse_moved)

    def figure_update(self, datas: Sequence[np.ndarray], labels: Sequence[str]):
        self.axes_labels = labels
        for item, data in zip(self.polarization_items, datas):
            item.update(data, labels)
