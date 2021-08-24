# * Imports
import math
import sys
from argparse import ArgumentParser

import matplotlib as mpl
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
    parser = HelpfulParser(
        description='Plot 2D resonance map for CO or CH3Cl. Clicking on a'
        ' resonance will print on standard output all pathways contributing to it.')
    parser.add_argument('molecule', choices=('CO', 'CH3Cl'),
                        help="Molecule.")
    parser.add_argument('-c', '--colors', type=int, choices=(1, 2, 3), default=3,
                        help="Full spectrum with broadband pulses or limited"
                        " to one or two colors (default: %(default)d).")
    parser.add_argument('-j', '--jmax', type=int,
                        help="Maximum initial angular momentum quantum number,")
    parser.add_argument('-d', '--direction', type=str, choices=["SI", "SII", "SII"],
                        help="Include only pathways phase-matched in a given direction."
                        "Direction is either `SI`, `SII` or `SIII` (default: %(default)s).")
    parser.add_argument('-f', "--filter", action='append',
                        help="Filter pathways by filtering excitation tree. "
                        "Can be provided multiple times to chain multiple filters.")
    parser.add_argument('-a', '--angles', nargs=4, default=[0.0]*4,
                        help="Three beam angles and the detection angle. "
                        "Each angle should either be a float, "
                        "'MA' for magic angle or 'Mug' for muggle angle."
                        "XXXX is the default polarization.")
    parser.add_argument('-t', '--time', type=float, default=1.0,
                        help="Waiting time in ps (default: %(default)f).")
    parser.add_argument('-D', '--dpi', type=float,
                        help="Force DPI.")
    args = parser.parse_args()
    angles = [parse_angle(angle) for angle in args.angles]
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
    meths = [getattr(pw, 'only_'+args.direction)]
    if args.colors == 2:
        meths.append(pw.remove_threecolor)
    elif args.colors == 1:
        meths.append(pw.only_dfwm)
    meths.extedn([getattr(pw, filter) for filter in args.filter])
# ** Calculate peaks
    pws = pw.gen_pathways(range(jmax), meths=meths,
                          rotor='symmetric' if args.molecule == 'CH3Cl' else 'linear',
                          kiter_func=lambda x: range(x))
    dressed_pws = dl.DressedPathway.from_kb_list(pws, vib_mode, T)
    peaks, dls = dl.peak_list(dressed_pws, return_dls=True, tw=args.time*1e-12, angles=angles)

# * Visualize
    fig_dict = vis.plot2d_scatter(peaks, scatter_kwargs=dict(picker=True))


    def scatter_onpick(event):
        """Show information about the peak pathway."""
        if event.artist != fig_dict['sc']:
            return
        dl.pprint_dllist(dls[event.ind[0]], abstract=True)


    fig_dict['fig'].canvas.mpl_connect('pick_event', scatter_onpick)
    plt.show()
