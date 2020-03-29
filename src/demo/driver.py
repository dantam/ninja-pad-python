import argparse
import logging

from demo.setenv import setenv
from demo.runenv import Simulation, simulate
from demo.shared_params import (
    add_shared_args,
    add_brownian_args,
    add_run_args,
    defaults
)

def get_args():
    parser = argparse.ArgumentParser(
        description="Setup and run simulation",
    )
    parser.add_argument(
        '--steps',
        default='all',
        help='comma separated options to select what to run. s: setup, r: run',
    )
    add_shared_args(parser)
    add_brownian_args(parser)
    add_run_args(parser)
    return parser.parse_args()

def drive(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    steps = args.steps.split(',')
    if 'all' in steps:
        steps = ['s', 'r']
    if 's' in steps:
        logging.debug('setting env')
        setenv(args)
        logging.debug('env ready')
    if 'r' in steps:
        logging.debug('simulate now')
        simulate(args)

def main():
    args = get_args()
    drive(args)

if __name__ == '__main__':
    main()
