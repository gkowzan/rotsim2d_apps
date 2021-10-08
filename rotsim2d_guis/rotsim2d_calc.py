"""Calculate list of 2D peaks of 2D spectrum"""
from pprint import pprint
import argparse
import sys
from argparse import ArgumentParser

import rotsim2d.dressedleaf as dl
import rotsim2d.pathways as pw
import rotsim2d.propagate as prop
import toml
from asteval import Interpreter


class HelpfulParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: {:s}\n'.format(message))
        self.print_help()
        sys.exit(2)


def run():
    parser = HelpfulParser(
        description="Calculate and save to file list of 2D peaks or 2D spectrum.",
        add_help=False)
    parser.add_argument("input_paths", nargs='+',
                        help="Paths to input files.",)
    args = parser.parse_args()
    aeval = Interpreter(use_numpy=False, minimal=True)
    for input_path in args.input_paths:
        params = toml.load(input_path)
        pprint(params)

        if str in [type(x) for x in params['spectrum']['angles']]:
            params['spectrum']['angles'] = \
                [aeval(angle) for angle in params['spectrum']['angles']]

        if params['spectrum']['type'] == 'peaks':
            print("Calculating peak list...")
            peaks = dl.run_peak_list(params)
            print("Saving to {!s}...".format(params['output']['file']))
            peaks.to_file(params['output']['file'],
                          metadata=params)
        elif params['spectrum']['type'] == 'lineshapes':
            print("Preparing DressedPathway's...")
            dls = dl.DressedPathway.from_params_dict(params['pathways'])
            print("Calculating 2D spectrum...")
            params = prop.run_update_metadata(params)
            fs_pu, fs_pr, spec2d = prop.run_propagate(
                dls, params['spectrum'])
            print("Saving to {!s}...".format(params['output']['file']))
            prop.run_save(
                params['output']['file'],
                fs_pu, fs_pr, spec2d,
                params)


if __name__ == '__main__':
    run()
