import argparse
import datetime
import json
import os

from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
    DatastoreTableNames as Tables,
)
from lib.configs.client_config import ClientConfig
from lib.crypto import Crypto
from demo.constants import Constants
from demo.shared_params import add_shared_args
from lib.clients.user_client import UserClient
from lib.configs.db_config import (
    ConfigFactory,
    DatastoreConfig,
)
from lib.auths.privacy_enforcer import (
    PrivacyEnforcer,
)

def get_args():
    parser = argparse.ArgumentParser(
        description="Run simulation",
    )
    parser.add_argument(
        '--num_days',
        default=10,
        help='number of days to simulate',
    )
    parser.add_argument(
        '--num_users',
        default=1,
        help='number of users',
    )
    parser.add_argument(
        '--user_log_frequency',
        default=60,
        help='number of logs per hour',
    )
    parser = add_shared_args(parser)
    return parser.parse_args()

class Simulation:
    def __init__(self, args):
        self.args = args
        self.users = {i: self.make_user() for i in range(args.num_users)}
        self.user_log_frequency = args.user_log_frequency
        self.num_days = args.num_days

    def make_user(self):
        client_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.client_config
        )
        db_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.db_config
        )
        db_config = DatastoreConfig(db_config)
        privacy_enforcer = PrivacyEnforcer(db_config)
        return UserClient(client_config, privacy_enforcer)

    def run(self):
        sim_log = []
        for day in range(self.num_days):
            self.run_users()
            self.run_medical_auths()
            self.run_medical_personal_auths()
            self.run_location_auths()
            self.run_location_auths_again()
            sim_log.append({
                'day': day,
            })
        return sim_log

    def run_users(self):
        for u in self.users.values():
            u.log_entry(datetime.datetime.now(), b'a')
        pass
    def run_medical_auths(self):
        pass
    def run_medical_personal_auths(self):
        pass
    def run_location_auths(self):
        pass
    def run_location_auths_again(self):
        pass

def simulate(args):
    sim = Simulation(args)
    log = sim.run()
    print(log)

def main():
    args = get_args()
    simulate(args)

if __name__ == '__main__':
    main()
