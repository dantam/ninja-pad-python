import argparse
import datetime
import json
import os
import random
import logging

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
    add_run_args,
)
from lib.configs.client_config import ClientConfig
from lib.clients.user_client import UserClient
from lib.configs.db_config import (
    ConfigFactory,
    DatastoreConfig,
)
from lib.auths.medical_auth import MedicalAuthorityClient
from lib.auths.location_auth import (
    LocationAuthority,
)
def get_args():
    parser = argparse.ArgumentParser(
        description="Run simulation",
    )

    add_shared_args(parser)
    add_brownian_args(parser)
    add_run_args(parser)
    return parser.parse_args()

class Simulation:
    def __init__(self, args):
        self.args = args
        self.set_configs()
        self.users = {i: self.make_user(i) for i in range(args.num_users)}
        self.auth_to_key_files = json.loads(args.auth_to_key_files)
        self.make_location_auth()

    def set_configs(self):
        self.user_client_configs = {}
        for uid in range(self.args.num_users):
            config = os.path.join(
                self.args.basedir,
                self.args.config_dir,
                self.args.client_config
            )
            config = '{}.{}'.format(config, uid)
            self.user_client_configs[uid] = config

        self.db_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.db_config
        )

    def make_user(self, uid):
        db_config = DatastoreConfig(self.db_config)
        self.med_client = MedicalAuthorityClient(db_config)
        return UserClient(self.user_client_configs[uid], db_config)

    def make_location_auth(self):
        db_config = DatastoreConfig(self.db_config)
        private_key_file = os.path.join(
            self.args.basedir,
            self.args.key_dir,
            Constants.LA_AUTH,
        )
        auth_id = self.auth_to_key_files[ClientConfig.LAS][0]
        self.location_auth = LocationAuthority(
            auth_id,
            self.user_client_configs[0], # to get other location auths
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
            self.users_check(today)
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

    def users_check(self, today):
        for i, user in enumerate(self.users.values()):
            start_time = today - datetime.timedelta(days=28)
            end_time = today + datetime.timedelta(days=1)
            if user.has_notification(start_time, end_time):
                logging.info('user {} notified on {}'.format(i, today))

def simulate(args):
    sim = Simulation(args)
    log = sim.run()
    logging.info(log)

def main():
    args = get_args()
    simulate(args)

if __name__ == '__main__':
    main()
