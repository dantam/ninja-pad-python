import os
import json

from argparse import Namespace
from lib.configs.client_config import ClientConfig
from demo.constants import Constants

auth_to_key_files = {
    ClientConfig.PAS: (1, Constants.PA_AUTH),
    ClientConfig.LAS: (2, Constants.LA_AUTH),
    ClientConfig.MAS: (3, Constants.MA_AUTH),
    ClientConfig.PES: (4, Constants.PE_AUTH),
}
auth_to_key_files_str = json.dumps(auth_to_key_files)

defaults = Namespace(
    basedir=os.path.join(os.getcwd(), Constants.BASE_DIR),
    config_dir=Constants.CONFIG_DIR,
    db_dir='dbs',
    db_config='db_conf.json',
    key_dir='keys',
    key_config='key_conf.json',
    client_config=Constants.CLIENT_CONFIG,
    num_users=1,
    one_time_pad_length=256,
    key_size=8192,
    public_exponent=65537,
    public_key_file_extension='pem',
    auth_to_key_files=auth_to_key_files_str,
    speed=2,
    xmin=0,
    xmax=100,
    numx=1,
    round=None,
    num_days=10,
    num_user_log_per_hour=60,
    num_patient_zeros=1,
)

def add_shared_args(parser):
    parser.add_argument(
        '--basedir',
        default=defaults.basedir,
        help='absolute path to directory',
    )
    parser.add_argument(
        '--config_dir',
        default=defaults.config_dir,
        help='relative path from basedir to config directory',
    )
    parser.add_argument(
        '--db_dir',
        default=defaults.db_dir,
        help='relative path from basedir to db directory',
    )
    parser.add_argument(
        '--db_config',
        default=defaults.db_config,
        help='name of output file',
    )
    parser.add_argument(
        '--key_dir',
        default=defaults.key_dir,
        help='relative path from basedir to key directory',
    )
    parser.add_argument(
        '--key_config',
        default=defaults.key_config,
        help='name of key file',
    )
    parser.add_argument(
        '--client_config',
        default=defaults.client_config,
        help='common name of client file (appended with user id)',
    )
    parser.add_argument(
        '--num_users',
        default=defaults.num_users,
        type=int,
        help='number of users',
    )
    parser.add_argument(
        '--one_time_pad_length',
        default=defaults.one_time_pad_length,
        type=int,
        help='number of bytes for one time pad',
    )
    parser.add_argument(
        '--key_size',
        default=defaults.key_size,
        type=int,
        help='number of bits for asymetric encryption key',
    )
    parser.add_argument(
        '--public_exponent',
        default=defaults.public_exponent,
        type=int,
        help='number of bits for asymetric encryption exponent',
    )
    parser.add_argument(
        '--public_key_file_extension',
        default=defaults.public_key_file_extension,
        help='postfix to public key files',
    )
    parser.add_argument(
        '--auth_to_key_files',
        default=defaults.auth_to_key_files,
        help='json dictionary for auth ids and keys',
    )
    parser.add_argument(
        '--debug',
        default=False,
        action='store_true',
        help='set log debug mode',
    )
    return parser

def add_brownian_args(parser):
    parser.add_argument(
        '--speed',
        default=defaults.speed,
        type=int,
        help='pos at time t is normal with mean x0, variance is delta**2*t',
    )
    parser.add_argument(
        '--xmin',
        default=defaults.xmin,
        type=int,
        help='minimum value of x',
    )
    parser.add_argument(
        '--xmax',
        default=defaults.xmax,
        type=int,
        help='max value of x',
    )
    parser.add_argument(
        '--numx',
        default=defaults.numx,
        type=int,
        help='number of x to simulate',
    )
    parser.add_argument(
        '--round',
        default=defaults.round,
        type=int,
        help='round at the last step',
    )
    return parser

def add_run_args(parser):
    parser.add_argument(
        '--num_days',
        default=defaults.num_days,
        help='number of days to simulate',
    )
    parser.add_argument(
        '--num_user_log_per_hour',
        default=defaults.num_user_log_per_hour,
        type=int,
        help='number of logs per hour',
    )
    parser.add_argument(
        '--num_patient_zeros',
        default=defaults.num_patient_zeros,
        type=int,
        help='number of patients zero in the system',
    )
    return parser
