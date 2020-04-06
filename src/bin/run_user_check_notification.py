import argparse
import datetime
import logging

from demo.shared_params import (
    add_shared_args,
    add_run_args,
)
from lib.clients.user_client_helper import UserClientHelper

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulate users fetching notification",
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

def get_notifications(args, users, start):
    notifications = {}
    for i, user in enumerate(users.values()):
        start_time = start - datetime.timedelta(days=1)
        end_time = start + datetime.timedelta(days=1)
        if user.has_notification(start_time, end_time):
            notifications[i] = True
    return notifications

def main():
    args = get_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    users = UserClientHelper.make_users(args)
    start = datetime.datetime.now() - datetime.timedelta(args.start_days_before)
    start = start + datetime.timedelta(args.days_from_start)
    notifications = get_notifications(args, users, start)
    print(notifications)

if __name__ == '__main__':
    main()
