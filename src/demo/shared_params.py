import os
import json

from lib.configs.client_config import ClientConfig
from demo.constants import Constants

def add_shared_args(parser):
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
        type=int,
        help='number of bytes for one time pad',
    )
    parser.add_argument(
        '--key_size',
        default=8192,
        type=int,
        help='number of bits for asymetric encryption key',
    )
    parser.add_argument(
        '--public_exponent',
        default=65537,
        type=int,
        help='number of bits for asymetric encryption exponent',
    )
    parser.add_argument(
        '--public_key_file_extension',
        default='pem',
        help='postfix to public key files',
    )

    auth_to_key_files = {
        ClientConfig.PAS: (1, Constants.PA_AUTH),
        ClientConfig.LAS: (2, Constants.LA_AUTH),
        ClientConfig.MAS: (3, Constants.MA_AUTH),
        ClientConfig.PES: (4, Constants.PE_AUTH),
    }
    parser.add_argument(
        '--auth_to_key_files',
        default=json.dumps(auth_to_key_files),
        help='json dictionary for auth ids and keys',
    )
    return parser

def add_brownian_args(parser):
    parser.add_argument(
        '--speed',
        default=2,
        type=int,
        help='pos at time t is normal with mean x0, variance is delta**2*t',
    )
    parser.add_argument(
        '--xmin',
        default=0,
        type=int,
        help='minimum value of x',
    )
    parser.add_argument(
        '--xmax',
        default=100,
        type=int,
        help='max value of x',
    )
    parser.add_argument(
        '--numx',
        default=1,
        type=int,
        help='number of x to simulate',
    )
    parser.add_argument(
        '--round',
        default=None,
        type=int,
        help='round at the last step',
    )
    return parser
