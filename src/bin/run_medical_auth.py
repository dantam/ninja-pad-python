import argparse
import datetime
import os
import json
import logging
import sys

from demo.shared_params import (
    add_shared_args,
    add_run_args,
)
from lib.auths.medical_auth import MedicalAuthorityClient
from lib.configs.db_config import DatastoreConfig
from lib.clients.user_client_helper import UserClientHelper

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulate medical authority confirming a new patient ",
    )
    parser.add_argument(
        '--patient_user_id',
        type=int,
        help="user ID ",
    )
    parser.add_argument(
        '--start_days_before',
        default=100,
        type=int,
        help="anchor for days before now to fetch used encrypted otps",
    )
    parser.add_argument(
        '--days_from_start',
        default=28,
        type=int,
        help="number of days after anchor to actually start",
    )
    add_shared_args(parser)
    add_run_args(parser)
    return parser.parse_args()

def make_medical_client(args):
    db_config = os.path.join(
        args.basedir,
        args.config_dir,
        args.db_config
    )
    db_config = DatastoreConfig(db_config)
    return MedicalAuthorityClient(db_config)

def main():
    args = get_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    db_config, user_configs = UserClientHelper.get_configs(args)
    user = UserClientHelper.make_user(
        args.patient_user_id,
        args,
        db_config,
        user_configs,
    )
    medical_client = make_medical_client(args)
    start = datetime.datetime.now() - datetime.timedelta(args.start_days_before)
    today = start + datetime.timedelta(days=args.days_from_start)
    payload = user.get_data_for_medical_auth(today)
    medical_client.upload(payload)


if __name__ == '__main__':
    main()

