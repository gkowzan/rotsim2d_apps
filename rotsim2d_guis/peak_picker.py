# * Imports
import math
import sys
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import rotsim2d.dressedleaf as dl
import rotsim2d.pathways as pw
import rotsim2d.visual as vis
from molspecutils.molecule import CH3ClAlchemyMode, COAlchemyMode


class HelpfulParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: {:s}\n'.format(message))
        self.print_help()
        sys.exit(2)

def parse_angle(angle: str) -> float:
    if angle == 'MA':
        return math.atan(math.sqrt(2))
    elif angle == 'Mug':
        return math.asin(2*math.sqrt(7)/7)
    else:
        return float(angle)


def run():
# * Parse arguments
    parser = HelpfulParser(description='Plot 2D resonance map for CO or CH3Cl. Clicking on a resonance will print on standard output all pathways contributing to it.')
    parser.add_argument('molecule', choices=('CO', 'CH3Cl'),
                        help="Molecule,")
    parser.add_argument('-c', '--colors', type=int, choices=(2, 3), default=3,
                        help="Mull spectrum with broadband pulses or limited to two colors (default: %(default)d),")
    parser.add_argument('-j', '--jmax', type=int,
                        help="Maximum initial angular momentum quantum number,")
    parser.add_argument('-d', '--direction', choices=("SI", "SII", "SIII"), default="SII",
                        help="Limit pathways to those emitted in selected direction (default: %(default)s).")
    parser.add_argument('-a', '--angles', nargs=4, default=[0.0]*4,
                        help="Three beam angles and the detection angle. Each angle should either be a float, 'MA' for magic angle or 'Mug' for muggle angle.")
    args = parser.parse_args()
    angles = [parse_angle(angle) for angle in args.angles]

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

    meths = [getattr(pw, 'only_'+args.direction)]
    pws = pw.gen_pathways(range(jmax), meths=meths,
                          rotor='symmetric' if args.molecule == 'CH3Cl' else 'linear',
                          kiter_func=lambda x: range(x if x<10 else 10))
    dressed_pws = dl.DressedPathway.from_kb_list(pws, vib_mode, T)
    peaks, dls = dl.peak_list(dressed_pws, return_dls=True, tw=1.0e-12, angles=angles)

# * Visualize
    fig_dict = vis.plot2d_scatter(peaks, scatter_kwargs=dict(picker=True))


    def scatter_onpick(event):
        """Show information about the peak pathway."""
        if event.artist != fig_dict['sc']:
            return
        dl.pprint_dllist(dls[event.ind[0]], abstract=True)


    fig_dict['fig'].canvas.mpl_connect('pick_event', scatter_onpick)
    plt.show()
