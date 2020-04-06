import argparse
import datetime
import json
import os
import random
import logging

from collections import defaultdict, Counter
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
from lib.clients.user_client_helper import UserClientHelper
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
        self.make_users()
        self.auth_to_key_files = json.loads(args.auth_to_key_files)
        self.make_location_auths()
        self.make_medical_auth()

    def set_configs(self):
        self.db_config = os.path.join(
            self.args.basedir,
            self.args.config_dir,
            self.args.db_config
        )

    def make_medical_auth(self):
        db_config = DatastoreConfig(self.db_config)
        self.med_client = MedicalAuthorityClient(db_config)

    def make_users(self):
        self.users = UserClientHelper.make_users(self.args)

    def make_location_auths(self):
        db_config = DatastoreConfig(self.db_config)
        self.location_auths = defaultdict()
        for auth_config in self.auth_to_key_files[ClientConfig.LAS]:
            private_key_file = os.path.join(
                self.args.basedir,
                self.args.key_dir,
                auth_config[1],
            )
            auth_id = auth_config[0]
            self.location_auths[auth_id] = LocationAuthority(
               auth_id,
               self.users[0].client_config, # to get other location auths
               db_config,
               private_key_file
            )

    def get_contaminated_contacts(self, xpos, ypos, new_diagnosed_patients):
        uid_locs = {}
        for p in new_diagnosed_patients:
            locs = []
            for loc in zip(xpos[p], ypos[p]):
                locs.append(loc)
            uid_locs[p] = locs

        uninfected_locs = {}
        for p in range(self.args.num_users):
            if p in new_diagnosed_patients:
                continue
            locs = []
            for loc in zip(xpos[p], ypos[p]):
                locs.append(loc)
            uninfected_locs[p] = locs

        contacts = defaultdict(list)
        for k, v in uid_locs.items():
            for ik, iv in uninfected_locs.items():
                for i, positions in enumerate(zip(v, iv)):
                    if positions[0] == positions[1]:
                        contacts[i].append((k, ik, positions[0]))

        logging.debug('carriers_locations:')
        for k, v in uid_locs.items():
            logging.debug('user {}: {}'.format(k, v))
        logging.debug('non_carriers_locations:')
        for k, v in uninfected_locs.items():
            logging.debug('user {}: {}'.format(k, v))

        return contacts

    def run(self):
        sim_log = []
        start = datetime.datetime.now() - datetime.timedelta(days=365)
        for day in range(self.args.num_days):
            logging.info('running simulation for day {}'.format(day))
            today = start + datetime.timedelta(days=day)
            xpos, ypos = self.simulate_users_positions(today)
            new_diagnosed_patients = self.run_medical_auths(today)
            location_auth_counters = self.run_location_auths(today)
            self.run_location_auths_again()
            users_notified = self.users_check(today)
            new_contacts = self.get_contaminated_contacts(
                xpos,
                ypos,
                new_diagnosed_patients,
            )
            sim_log.append({
                'day': day,
                'xpos': xpos,
                'ypos': ypos,
                'new_diagnosed_patients': new_diagnosed_patients,
                'users_notified': users_notified,
                'new_contacts': new_contacts,
                **location_auth_counters,
            })
        return sim_log

    def brownian(self):
        return brownian(
            len(self.users),
            24 * self.args.num_user_log_per_hour, # num steps
            24 * 60, # total time
            self.args.speed,
            self.args.xmin,
            self.args.xmax,
            self.args.round,
        )

    def simulate_users_positions(self, today):
        xpos = self.brownian()
        ypos = self.brownian()
        num_entries = len(xpos[0, 1:])
        delta_seconds = 60 * 60 * 24 / num_entries
        for i, u in enumerate(self.users.values()):
            step = 0
            for x, y in zip(xpos[i, :], ypos[i, :]):
                delta_time = datetime.timedelta(seconds=delta_seconds * step)
                step += 1
                log_time = today + delta_time
                u.process_one_position(log_time, x, y)
        return (xpos, ypos)

    def run_medical_auths(self, today):
        new_patients = []
        for i, u in enumerate(self.users.values()):
            if i < self.args.num_patient_zeros:
                payload = u.get_data_for_medical_auth(today)
                self.med_client.upload(payload)
                new_patients.append(i)
        return new_patients

    def run_location_auths(self, today):
        endtime = today + datetime.timedelta(days=1)
        counter = Counter()
        for auth in self.location_auths.values():
            counter.update(auth.process_contaminations(today, endtime))
        return counter

    def run_location_auths_again(self):
        pass

    def users_check(self, today):
        notifications = []
        for i, user in enumerate(self.users.values()):
            start_time = today - datetime.timedelta(days=28)
            end_time = today + datetime.timedelta(days=1)
            if user.has_notification(start_time, end_time):
                notifications.append(i)
        return notifications

def simulate(args):
    sim = Simulation(args)
    logging.info('running simulation')
    log = sim.run()
    debug_print_log(log)
    return log

def debug_print_log(log):
    filtered = ['xpos', 'ypos']
    for d in log:
        payload = {k: d[k] for k in d.keys() if k not in filtered}
        logging.debug(payload)

def main():
    args = get_args()
    simulate(args)

if __name__ == '__main__':
    main()
