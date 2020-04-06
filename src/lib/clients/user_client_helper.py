import os
from lib.configs.db_config import DatastoreConfig
from lib.clients.user_client import UserClient

class UserClientHelper:
    def get_configs(args):
        db_config = os.path.join(
            args.basedir,
            args.config_dir,
            args.db_config
        )
        user_configs = UserClientHelper.make_user_configs(args)
        db_config = DatastoreConfig(db_config)
        return db_config, user_configs

    def make_users(args):
        db_config, user_configs = UserClientHelper.get_configs(args)
        return {i: UserClientHelper.make_user(i, args, db_config, user_configs)
            for i in range(args.num_users)
        }

    def make_user_configs(args):
        user_client_configs = {}
        for uid in range(args.num_users):
            config = os.path.join(
                args.basedir,
                args.config_dir,
                args.client_config
            )
            config = '{}.{}'.format(config, uid)
            user_client_configs[uid] = config
        return user_client_configs

    def make_user(uid, args, db_config, user_configs):
        return UserClient(
            user_configs[uid],
            db_config,
            public_exponent=args.public_exponent,
            key_size=args.key_size,
        )

