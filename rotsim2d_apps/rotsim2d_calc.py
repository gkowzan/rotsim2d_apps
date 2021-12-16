"""Calculate list of 2D peaks of 2D spectrum"""
import string
import sys
from argparse import ArgumentParser
from pprint import pprint
from typing import List, Sequence

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


def named_fields(s: str) -> List[str]:
    return [x[1] for x in string.Formatter().parse(s)
            if x[1] is not None]


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
        elif params['spectrum']['type'] in ('lineshapes', 'time'):
            print("Preparing DressedPathway's...")
            dls = dl.DressedPathway.from_params_dict(params['pathways'])
            print("Calculating 2D spectrum...")
            params = prop.run_update_metadata(params)

            if isinstance(params['spectrum']['pressure'], Sequence) and\
               'p' not in named_fields(params['output']['file']):
                raise ValueError(
                    "Format specifier with field 'p' not provided. "
                    "Data for all pressures would have been overwritten.")

            if not isinstance(params['spectrum']['pressure'], Sequence):
                pressures = [params['spectrum']['pressure']]
            else:
                pressures = params['spectrum']['pressure'][:]
            for p in pressures:
                params['spectrum']['pressure'] = p
                print("Pressure = {:.2f} atm".format(p))
                fs_pu, fs_pr, spec2d = prop.run_propagate(
                    dls, params['spectrum'])
                output_file = params['output']['file'].format(p=p)
                print("Saving to {!s}...".format(output_file))
                prop.run_save(
                    output_file,
                    fs_pu, fs_pr, spec2d,
                    params)


if __name__ == '__main__':
    run()
