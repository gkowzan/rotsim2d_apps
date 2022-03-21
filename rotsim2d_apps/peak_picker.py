# * Imports
import argparse
import math
import sys
from argparse import ArgumentParser

from asteval import Interpreter
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import rotsim2d.dressedleaf as dl
import rotsim2d.pathways as pw
import rotsim2d.visual as vis
from matplotlib.colorbar import Colorbar
from molspecutils.molecule import CH3ClAlchemyMode, COAlchemyMode


class HelpfulParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: {:s}\n'.format(message))
        self.print_help()
        sys.exit(2)


def run():
# * Parse arguments
    parser = HelpfulParser(
        description='Plot 2D resonance map of 2D spectrum of CO or CH3Cl.'
        ' Clicking on a resonance will print on standard output all pathways'
        ' contributing to it.',
        add_help=False)
    parser.add_argument('molecule', choices=('CO', 'CH3Cl'),
                        help="Molecule.")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-c', '--colors', type=int, choices=(1, 2, 3), default=3,
                        help="Full spectrum with broadband pulses or limited"
                        " to one or two colors (default: %(default)d).")
    parser.add_argument('-j', '--jmax', type=int,
                        help="Maximum initial angular momentum quantum number.")
    parser.add_argument('-k', '--kmax', type=int,
                        help="Maximum projection on principal molecular axis.")
    parser.add_argument('--no-abstract', action='store_true',
                        help='Print actual J values.')
    parser.add_argument('-f', "--filter", action='append',
                        help="Filter pathways by filtering excitation tree. "
                        "Can be provided multiple times to chain multiple filters.")
    parser.add_argument('-a', '--angles', nargs=4, default=['0.0']*4,
                        help="Three beam angles and the detection angle. "
                        "Each angle can be a Python mathematical expression"
                        " using standard arithmetic operators and math"
                        " functions from Python math module.")
    parser.add_argument('-t', '--time', type=float, default=1.0,
                        help="Waiting time in ps (default: %(default)f).")
    parser.add_argument('-D', '--dpi', type=float,
                        help="Force DPI.")
    parser.add_argument('--symmetric-log', action='store_true',
                        help="Use symmetric logarithmic scaling for color"
                        " normalization.")
    args = parser.parse_args()

    aeval = Interpreter(use_numpy=False, minimal=True)
    angles = [aeval(angle) for angle in args.angles]
    if args.dpi:
        mpl.rcParams['figure.dpi'] = args.dpi

# * Vibrational mode
    print('Initializing vibrational mode')
    if args.molecule == 'CH3Cl':
        vib_mode = CH3ClAlchemyMode()
    else:
        vib_mode = COAlchemyMode()
    T = 296.0

# * Pathways
    print('Calculating peak list')
    jmax = args.jmax
    if jmax is None:
        if args.molecule == 'CH3Cl':
            jmax = 37
        else:
            jmax = 20

# ** Filters
    meths = []
    if args.colors == 2:
        meths.append(pw.remove_threecolor)
    elif args.colors == 1:
        meths.append(pw.only_dfwm)
    if args.filter:
        meths.extend([getattr(pw, filter) for filter in args.filter])
# ** Calculate peaks
    if args.kmax:
        kiter_func = "range((j if j<={kmax:d} else {kmax:d})+1)".format(kmax=args.kmax)
    else:
        kiter_func = "range(j+1)"
    pws = pw.gen_pathways(
        range(jmax), meths=meths,
        rotor='symmetric' if args.molecule == 'CH3Cl' else 'linear',
        kiter_func=kiter_func)
    dressed_pws = dl.DressedPathway.from_kb_list(pws, vib_mode, T)
    peaks = dl.Peak2DList.from_dp_list(
        dressed_pws, tw=args.time*1e-12, angles=angles)
    vminmax = np.max(np.abs(np.array(peaks.intensities)))*1.1*1e6

# * Visualize
    if args.symmetric_log:
        norm = colors.SymLogNorm(linthresh=vminmax/100.0,
                                 vmin=-vminmax, vmax=vminmax)
    else:
        norm = colors.Normalize(vmin=-vminmax, vmax=vminmax)

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[20, 1])
    ax = fig.add_subplot(gs[0])
    sc = ax.scatter(peaks.probes, peaks.pumps, s=10.0,
                    c=np.array(peaks.intensities)*1e6,
                    cmap='seismic', norm=norm, picker=True)
    ax.set(xlabel=r'$\Omega_3$ (cm$^{-1}$)',
           ylabel=r'$\Omega_1$ (cm$^{-1}$)')

    axcbar = fig.add_subplot(gs[-1])
    cbar = Colorbar(mappable=sc, ax=axcbar, orientation='vertical', extend='neither')
    amp_str = r"$S^{(3)}\cos \Omega_2 t_2$"
    cbar.set_label(amp_str + r" ($10^{-6}$ m$^{2}$ Hz/(V s/m)$^2$)")

    ax.set_title(str(args.filter), fontsize=10)
    fig.canvas.set_window_title(str(args.filter))

    abstract = not args.no_abstract
    def scatter_onpick(event):
        """Show information about the peak pathway."""
        if event.artist != sc:
            return
        dl.pprint_dllist(peaks[event.ind[0]].dp_list, abstract=abstract, angles=angles)


    fig.canvas.mpl_connect('pick_event', scatter_onpick)
    plt.show()
