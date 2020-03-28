import os

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
        help='number of bytes for one time pad',
    )
    parser.add_argument(
        '--key_size',
        default=8192,
        help='number of bits for asymetric encryption key',
    )
    parser.add_argument(
        '--public_exponent',
        default=65537,
        help='number of bits for asymetric encryption exponent',
    )
    parser.add_argument(
        '--public_key_file_extension',
        default='pem',
        help='postfix to public key files',
    )
    return parser
