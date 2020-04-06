import argparse
import datetime

from demo.brownian import brownian
from demo.shared_params import (
    add_shared_args,
    add_brownian_args,
    add_run_args,
)

import numpy as np

def get_args():
    parser = argparse.ArgumentParser(
        description="Make user locations",
    )
    parser.add_argument(
        '--output_file',
        default='/tmp/user_locations.txt',
        help="file for storing user locations, in delimited format",
    )
    parser.add_argument(
        '--delim',
        default='\t',
        help="delimiter between fields",
    )
    parser.add_argument(
        '--start_days_before',
        default=100,
        type=int,
        help="number of days before now to simulate locations",
    )
    add_shared_args(parser)
    add_brownian_args(parser)
    add_run_args(parser)
    return parser.parse_args()

def run_brownian(args):
    return brownian(
        args.num_users,
        24 * args.num_user_log_per_hour, # num steps
        24 * 60, # total time
        args.speed,
        args.xmin,
        args.xmax,
        args.round,
    )

def make_user_locations(args):
    start = datetime.datetime.now() - datetime.timedelta(args.start_days_before)
    entries = []
    delta_seconds = 60 * 60 / args.num_user_log_per_hour
    for day in range(args.num_days):
        for user in range(args.num_users):
            xpos = run_brownian(args)
            ypos = run_brownian(args)
            step = 0
            for x, y in zip(xpos[user, :], ypos[user, :]):
                delta_time = datetime.timedelta(seconds=delta_seconds * step)
                time = start + datetime.timedelta(day) + delta_time
                entries.append((user, time, x, y))
                step += 1
    lines = [args.delim.join(map(str, entry)) for entry in entries]
    payload = '\n'.join(lines)
    with open(args.output_file, 'w') as f:
        f.write(payload)

def main():
    args = get_args()
    make_user_locations(args)

if __name__ == '__main__':
    main()
