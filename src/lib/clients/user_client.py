import secrets

from collections import defaultdict
from lib.configs.client_config import ClientConfig
from lib.configs.authority_public_keys_config import (
    AuthorityPublicKeysConfig as APKC,
)
from lib.auths.privacy_enforcer import (
    PrivacyEnforcerClient,
)

class UserClient:
    def __init__(self, client_config, privacy_enforcer):
        self.client_config = ClientConfig(client_config)
        self.public_keys_config = APKC(
            self.client_config.get_public_keys_file()
        )
        self.crypto_clients = defaultdict(defaultdict)
        self.privacy_enforcer = privacy_enforcer

    def get_crypto_client(self, auth_type, auth_id):
        if auth_id in self.crypto_clients[auth_type]:
            return self.crypto_clients[auth_type][auth_id]

        public_key = self.public_keys_config.get_public_key(
            auth_type,
            auth_id,
        )
        self.crypto_clients[auth_type][auth_id] = public_key
        return self.crypto_clients[auth_type][auth_id]

    def encrypt_one_time_pad(self):
        otp = secrets.token_hex(self.client_config.get_one_time_pad_length())
        pa_id = self.client_config.get_person_auth()
        crypto_client = self.get_crypto_client(ClientConfig.PAS, pa_id)
        return crypto_client.encrypt(otp.encode())

    def encrypt_location(self, location):
        la_id = self.client_config.get_location_auth()
        crypto_client = self.get_crypto_client(ClientConfig.LAS, la_id)
        return crypto_client.encrypt(location)

    def log_entry(self, time, location):
        pe_client = PrivacyEnforcerClient(self.privacy_enforcer)
        return pe_client.upload(
            time,
            self.encrypt_location(location),
            self.encrypt_one_time_pad(),
        )
