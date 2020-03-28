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
from demo.constants import Constants

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
        default='{}/{}/'.format(os.getcwd(), Constants.BASE_DIR),
        help='absolute path to directory',
    )
    parser.add_argument(
        '--config_dir',
        default=Constants.CONFIG_DIR,
        help='relative path from basedir to config directory',
    )
    parser.add_argument(
        '--db_dir',
        default='dbs',
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
        default=Constants.CLIENT_CONFIG,
        help='name of client file',
    )
    parser.add_argument(
        '--one_time_pad_length',
        default=256,
        help='number of bytes for one time pad',
    )
    parser.add_argument(
        '--public_key_file_extension',
        default='pem',
        help='postfix to public key files',
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
        ClientConfig.ONE_TIME_PAD_LENGTH: args.one_time_pad_length,
        ClientConfig.PUBLIC_KEYS_FILE: keys_file,
    }
    payload.update(auth_to_auth_ids)
    write_file(args, payload, args.client_config)

auth_to_key_files = {
    ClientConfig.PAS: (1, 'pa_auth'),
    ClientConfig.LAS: (2, 'la_auth'),
    ClientConfig.MAS: (3, 'ma_auth'),
    ClientConfig.PES: (4, 'pe_auth'),
}

def make_key_config_file(args):
    key_config = {}
    for k, v in auth_to_key_files.items():
        auth_id, filename = v
        filename = '{}.{}'.format(filename, args.public_key_file_extension)
        fullpath = os.path.join(args.basedir, args.key_dir, filename)
        key_config[k] = {auth_id: fullpath}
    write_file(args, key_config, args.key_config)

def make_config_files(args):
    make_db_config_file(args)
    make_client_config_file(args)
    make_key_config_file(args)

def make_keys(args):
    for k, v in auth_to_key_files.items():
        auth_id, filename = v
        pub_file = '{}.{}'.format(filename, args.public_key_file_extension)
        crypto = Crypto()
        fullpath = os.path.join(args.basedir, args.key_dir, pub_file)
        crypto.public_key_to_file(fullpath)
        fullpath = os.path.join(args.basedir, args.key_dir, filename)
        crypto.UNSAFE_private_key_to_file(fullpath)

def main():
    args = get_args()
    make_config_files(args)
    make_keys(args)

if __name__ == '__main__':
    main()
