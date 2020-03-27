import argparse
import json
import os

from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
    DatastoreTableNames as Tables,
)
from lib.configs.client_config import ClientConfig

store_to_files = {
    DC.ON_DEVICE_STORE: Tables.ON_DEVICE_STORE,
    DC.LOCATION_LOGS: Tables.LOCATION_LOG,
    DC.NOTIFICATION_LOGS: Tables.NOTIFICATION_LOG,
    DC.CONTAMINATION_LOGS: Tables.CONTAMINATION_LOG,
    DC.PRIVACY_ENFORCER_STORE: Tables.PRIVACY_ENFORCER_STORE,
}

def get_args():
    parser = argparse.ArgumentParser(
        description="Set up database config",
    )
    parser.add_argument(
        '--basedir',
        default='{}/demo/'.format(os.getcwd()),
        help='absolute path to directory',
    )
    parser.add_argument(
        '--config_dir',
        default='configs'.format(os.getcwd()),
        help='relative path from basedir to config directory',
    )
    parser.add_argument(
        '--db_dir',
        default='dbs'.format(os.getcwd()),
        help='relative path from basedir to db directory',
    )
    parser.add_argument(
        '--db_config',
        default='db_conf.json',
        help='name of output file',
    )
    parser.add_argument(
        '--key_dir',
        default='keys'.format(os.getcwd()),
        help='relative path from basedir to key directory',
    )
    parser.add_argument(
        '--key_config',
        default='key_conf.json',
        help='name of key file',
    )
    return parser.parse_args()

def write_file(args, payload, filename):
    fullpath = os.path.join(args.basedir, args.config_dir, filename)
    with open(fullpath, 'w') as f:
        f.write(json.dumps(payload, indent=4, sort_keys=True))

def make_db_config_file(args):
    db_config = {}
    for k, v in store_to_files.items():
        db_config[k] = [{
            DC.DATABASE_ENGINE: DE.SQLITE,
            DC.DATABASE_FILE: os.path.join(args.basedir, args.db_dir, v),
        }]
    write_file(args, db_config, args.db_config)

auth_to_key_files = {
    ClientConfig.PAS: 'pa_auth',
    ClientConfig.LAS: 'la_auth',
    ClientConfig.MAS: 'ma_auth',
    ClientConfig.PES: 'pe_auth',
}
def make_key_config_file(args):
    key_config = {}
    key_id = 1
    for k, v in auth_to_key_files.items():
        key_config[k] = {key_id: v}
        key_id += 1
    write_file(args, key_config, args.key_config)

def make_config_files(arg):
    make_db_config_file(arg)
    make_key_config_file(arg)

def main():
    args = get_args()
    make_config_files(args)

if __name__ == '__main__':
    main()
