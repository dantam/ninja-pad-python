import argparse
import datetime
import os
import logging
import sys
import numpy as np

from demo.shared_params import (
    add_shared_args,
    add_run_args,
)
from lib.clients.user_client_helper import UserClientHelper

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulate users uploading locations",
    )
    parser.add_argument(
        '--input_file',
        default=None,
        help="file storing user locations, in delimited format",
    )
    parser.add_argument(
        '--delim',
        default='\t',
        help="delimiter between fields",
    )
    add_shared_args(parser)
    return parser.parse_args()

def load_user_positions(args):
    fh = sys.stdin
    if args.input_file is not None and args.input_file != '-':
        fh = open(args.input_file, 'r')

    with fh as f:
        for line in f:
            uid, time, x, y = line.strip().split(args.delim)
            yield uid, time, x, y

def process_user_positions(args, users):
    num_entries = 0
    for uid, time, x, y in load_user_positions(args):
        user = users[int(uid)]
        time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        user.process_one_position(time, x, y)
        num_entries += 1
    return num_entries

def main():
    args = get_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    users = UserClientHelper.make_users(args)
    num_entries = process_user_positions(args, users)
    logging.debug('uploaded {} entries'.format(num_entries))

if __name__ == '__main__':
    main()
