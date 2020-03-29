import argparse
import datetime
import json
import os
import random

from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
    DatastoreTableNames as Tables,
)
from demo.constants import Constants
from demo.brownian import brownian
from demo.shared_params import (
    add_shared_args,
    add_brownian_args,
)
from lib.configs.client_config import ClientConfig
from lib.clients.user_client import UserClient
from lib.configs.db_config import (
    ConfigFactory,
    DatastoreConfig,
)
from lib.datastores.on_device_store import OnDeviceStore
from lib.auths.privacy_enforcer import PrivacyEnforcer
from lib.auths.medical_auth import MedicalAuthorityClient
from lib.auths.location_auth import (
    LocationAuthority,
    LocationAuthorityCrypto,
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
        type=int,
        help='number of logs per hour',
    )
    parser.add_argument(
        '--patient_zero_prob',
        default=0.001,
        type=float,
        help='probability user catches from without contact',
    )

    parser = add_shared_args(parser)
    parser = add_brownian_args(parser)
    return parser.parse_args()

class Simulation:
    def __init__(self, args):
        self.args = args
        self.set_configs()
        self.users = {i: self.make_user() for i in range(args.num_users)}
        args.auth_to_key_files = json.loads(args.auth_to_key_files)
        self.make_location_auth()

    def set_configs(self):
        self.client_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.client_config
        )
        self.db_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.db_config
        )

    def make_user(self):
        db_config = DatastoreConfig(self.db_config)
        privacy_enforcer = PrivacyEnforcer(db_config)
        self.med_client = MedicalAuthorityClient(db_config)
        on_device_store = OnDeviceStore(db_config)
        return UserClient(self.client_config, privacy_enforcer, on_device_store)

    def make_location_auth(self):
        db_config = DatastoreConfig(self.db_config)
        private_key_file = os.path.join(
            self.args.basedir,
            self.args.key_dir,
            Constants.LA_AUTH,
        )
        auth_id = self.args.auth_to_key_files[ClientConfig.LAS][0]
        self.location_auth = LocationAuthority(
            auth_id,
            self.client_config,
            db_config,
            private_key_file
        )

    def run(self):
        sim_log = []
        start = datetime.datetime.now() - datetime.timedelta(days=365)
        for day in range(self.args.num_days):
            today = start + datetime.timedelta(days=day)
            self.run_users(today)
            self.run_medical_auths()
            self.run_location_auths(today)
            self.run_location_auths_again()
            sim_log.append({
                'day': day,
            })
        return sim_log

    def brownian(self):
        return brownian(
            len(self.users),
            24 * self.args.user_log_frequency, # num steps
            24 * 60, # total time
            self.args.speed, # speed
            0,  # min val
            1000, # max val
            0 # round to int
        )

    def run_users(self, today):
        xpos = self.brownian()
        ypos = self.brownian()
        num_entries = len(xpos[0, 1:])
        delta_seconds = 60 * 60 * 24 / num_entries
        for i, u in enumerate(self.users.values()):
            log_time = today + datetime.timedelta(seconds=delta_seconds * i)
            for x, y in zip(xpos[i, 1:], ypos[i, 1:]):
                location = '{}:{}'.format(x, y)
                otp, pa_id = u.encrypt_one_time_pad()
                u.log_entry(log_time, location.encode(), otp)
                u.log_private_entry(log_time, otp, pa_id)

    def run_medical_auths(self):
        for i, u in enumerate(self.users.values()):
            if random.random() < self.args.patient_zero_prob:
                pa_id = u.get_a_person_auth_id()
                payload = u.get_data_for_medical_auth(pa_id)[0]
                self.med_client.upload(payload.time, payload.salted_otp)

    def run_location_auths(self, today):
        endtime = today + datetime.timedelta(days=1)
        self.location_auth.process_contaminations(today, endtime)

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
