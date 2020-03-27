import argparse
import json
import os

from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
    DatastoreTableNames as Tables,
)

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
    return parser.parse_args()

def make_config_file(args):
    db_config = {}
    for k, v in store_to_files.items():
        db_config[k] = [{
            DC.DATABASE_ENGINE: DE.SQLITE,
            DC.DATABASE_FILE: os.path.join(args.basedir, args.db_dir, v),
        }]

    fullpath = os.path.join(args.basedir, args.config_dir, args.db_config)
    with open(fullpath, 'w') as f:
        f.write(json.dumps(db_config, indent=4, sort_keys=True))

def main():
    args = get_args()
    make_config_file(args)

if __name__ == '__main__':
    main()
