import argparse
import datetime
import os
import json
import logging
import sys
import numpy as np

from demo.shared_params import (
    add_shared_args,
    add_run_args,
)
from lib.configs.client_config import ClientConfig
from lib.configs.db_config import DatastoreConfig
from lib.auths.location_auth import LocationAuthority

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulate location authorities processing location log",
    )
    parser.add_argument(
        '--start_days_before',
        default=100,
        type=int,
        help="number of days before now to process locations",
    )
    parser.add_argument(
        '--end_days_from_start',
        default=1,
        type=int,
        help="number of days after start day to process locations",
    )
    add_shared_args(parser)
    return parser.parse_args()

def setup_location_authorities(args):
    location_auths = {}
    auth_to_key_files = json.loads(args.auth_to_key_files)
    configs = auth_to_key_files[ClientConfig.LAS]
    db_config = os.path.join(
        args.basedir,
        args.config_dir,
        args.db_config
    )
    db_config = DatastoreConfig(db_config)
    client_config = os.path.join(
        args.basedir,
        args.config_dir,
        '{}{}'.format(args.client_config, '.0'),
    )
    for config in configs:
        auth_id = config[0]
        private_key_file = os.path.join(
            args.basedir,
            args.key_dir,
            config[1],
        )
        location_auths[auth_id] = LocationAuthority(
            auth_id,
            ClientConfig(client_config),
            db_config,
            private_key_file,
        )
    return location_auths

def run_location_authorities(args, local_auths):
    start = datetime.datetime.now() - datetime.timedelta(args.start_days_before)
    end = start + datetime.timedelta(days=args.end_days_from_start)
    for auth_id, auth in local_auths.items():
        auth.process_contaminations(start, end)

def main():
    args = get_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    location_auths = setup_location_authorities(args)
    run_location_authorities(args, location_auths)

if __name__ == '__main__':
    main()
