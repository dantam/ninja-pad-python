import json

from collections import defaultdict
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from lib.crypto import CryptoClient

class AuthorityPublicKeysConfig:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)
        self.public_keys = defaultdict(dict)

    def get_public_auth_ids(self, auth_type):
        return self.config[auth_type].keys()

    def get_public_key_value(self, auth_type, auth_id):
        return self.config[auth_type][auth_id]

    def get_public_key(self, auth_type, auth_id):
        auth_type_keys = self.public_keys[auth_type]
        if auth_id in auth_type_keys:
            return auth_type_keys[auth_id]

        filename = self.get_public_key_value(auth_type, str(auth_id))
        crypto_client = CryptoClient(filename)
        auth_type_keys[auth_id] = crypto_client
        return auth_type_keys[auth_id]
