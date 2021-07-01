# -*- coding: utf-8 -*-
from contextlib import contextmanager
from PyQt5 import QtGui, QtWidgets
import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.colors as clrs
from matplotlib.colorbar import Colorbar
from matplotlib.widgets import MultiCursor


class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(frameon=False)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class PolarizationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, parent)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
        self.fig = self.canvas.fig
        self.figure_setup()

    @staticmethod
    def main_subplots(gs):
        for ss in gs:
            if ss.is_last_col():
                continue
            else:
                yield ss

    def figure_setup(self):
        # self.fig.patch.set_facecolor('white')
        fake_data = np.zeros((100, 100))
        self.gs = self.fig.add_gridspec(
            nrows=2, ncols=5, width_ratios=[20, 20, 20, 20, 1])
        subplots = list(self.main_subplots(self.gs))
        del subplots[3]
        self.axes = [self.fig.add_subplot(subplots[i]) for i in range(7)]
        axcbar = self.fig.add_subplot(self.gs[:, -1])
        scalar_map = cm.ScalarMappable(norm=clrs.Normalize(-1, 1),
                                       cmap=cm.get_cmap('RdBu'))
        cbar = Colorbar(mappable=scalar_map,
                        ax=axcbar, orientation='vertical', extend='neither')
        extent = [-90, 90, -90, 90]
        self.images = [self.axes[i].imshow(
            fake_data, aspect='auto', extent=extent, origin='lower', vmin=-1.0,
            vmax=1.0, cmap=cm.get_cmap('RdBu')) for i in range(7)]
        self.blit_manager = BlitManager(self.canvas, self.images)
        self.multicursor = MultiCursor(
            self.canvas, self.axes, useblit=True, horizOn=True, vertOn=True,
            color='gray', lw=0.7)
        self.canvas.mpl_connect('figure_leave_event', self.restore_main_blit)
        self.canvas.mpl_connect('figure_enter_event', self.disable_main_blit)

    def set_titles(self, titles):
        for title, ax in zip(titles, self.axes):
            ax.set_title(title, fontsize=8)

    def disable_main_blit(self, event):
        for art in self.blit_manager._artists:
            art.set_animated(False)
        self.canvas.draw()
        # for line in self.multicursor.vlines + self.multicursor.hlines:
        #     line.set_visible(True)

    def restore_main_blit(self, event):
        for art in self.blit_manager._artists:
            art.set_animated(True)
        # for line in self.multicursor.vlines + self.multicursor.hlines:
        #     line.set_visible(False)
        self.canvas.restore_region(self.multicursor.background)
        self.canvas.blit()

    def figure_update(self, data):
        """`data` is a list of 2D arrays."""
        for i in range(7):
            self.images[i].set_data(data[i])
        self.blit_manager.update()
