import argparse
import json
import os

from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
    DatastoreTableNames as Tables,
)
from lib.configs.client_config import ClientConfig
from lib.crypto import Crypto

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
    parser.add_argument(
        '--client_config',
        default='client_conf.json',
        help='name of client file',
    )
    parser.add_argument(
        '--token_length',
        default=256,
        help='number of bytes for secrets',
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

auth_to_auth_ids = {
    ClientConfig.PAS: [1],
    ClientConfig.LAS: [2],
    ClientConfig.MAS: [3],
    ClientConfig.PES: [4],
}
def make_client_config_file(args):
    keys_file = os.path.join(args.basedir, args.config_dir, args.key_config)
    payload = {
        ClientConfig.TOKEN_LENGTH: args.token_length,
        ClientConfig.PUBLIC_KEYS_FILE: keys_file,
    }
    payload.update(auth_to_auth_ids)
    write_file(args, payload, args.client_config)

auth_to_key_files = {
    ClientConfig.PAS: (1, 'pa_auth.pem'),
    ClientConfig.LAS: (2, 'la_auth.pem'),
    ClientConfig.MAS: (3, 'ma_auth.pem'),
    ClientConfig.PES: (4, 'pe_auth.pem'),
}
def make_key_config_file(args):
    key_config = {}
    for k, v in auth_to_key_files.items():
        auth_id, filename = v
        fullpath = os.path.join(args.basedir, args.key_dir, filename)
        key_config[k] = {auth_id: fullpath}
    write_file(args, key_config, args.key_config)
    return key_config

def make_config_files(args):
    make_db_config_file(args)
    make_client_config_file(args)
    key_config = make_key_config_file(args)
    return key_config

def make_keys(args, key_config):
    for k in key_config.keys():
        for v in key_config[k].values():
            crypto = Crypto()
            crypto.public_key_to_file(v)

def main():
    args = get_args()
    key_config = make_config_files(args)
    make_keys(args, key_config)

if __name__ == '__main__':
    main()
