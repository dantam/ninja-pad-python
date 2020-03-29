import datetime
import secrets

from collections import defaultdict
from lib.configs.client_config import ClientConfig
from lib.configs.authority_public_keys_config import (
    AuthorityPublicKeysConfig as APKC,
)
from lib.auths.privacy_enforcer import (
    PrivacyEnforcerClient,
)
from lib.datastores.notification_log import NotificationLog
from lib.datastores.on_device_store import OnDeviceStore
from lib.auths.privacy_enforcer import PrivacyEnforcer

class UserClient:
    def __init__(self, client_config, db_config):
        self.privacy_enforcer = PrivacyEnforcer(db_config)
        self.notification_log = NotificationLog(db_config)

        self.client_config = ClientConfig(client_config)
        on_device_store_config = self.client_config.get_on_device_config()
        self.on_device_store = OnDeviceStore(on_device_store_config)

        self.public_keys_config = APKC(
            self.client_config.get_public_keys_file()
        )
        self.crypto_clients = defaultdict(defaultdict)

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
        return crypto_client.encrypt(otp.encode()), pa_id

    def encrypt_location(self, location):
        la_id = self.client_config.get_location_auth()
        crypto_client = self.get_crypto_client(ClientConfig.LAS, la_id)
        return crypto_client.encrypt(location)

    def log_entry(self, time, location, encrypted_otp):
        pe_client = PrivacyEnforcerClient(self.privacy_enforcer)
        return pe_client.upload(
            time,
            self.encrypt_location(location),
            encrypted_otp,
        )

    def log_private_entry(self, time, salted_otp, person_auth_id):
        return self.on_device_store.insert(
            time,
            salted_otp,
            person_auth_id,
        )

    def get_a_person_auth_id(self):
        return self.client_config.get_person_auth()

    def get_data_for_medical_auth(self, personal_auth_id):
        return self.on_device_store.get_latest(personal_auth_id)

    def has_notification(self, start_time, end_time):
        notices = self.notification_log.query(
            (start_time, end_time)
        )
        for notice in notices:
            matches = self.on_device_store.query(
                (notice.time - datetime.timedelta(seconds=120),
                 notice.time + datetime.timedelta(seconds=120)),
                salted_otp=notice.encrypted_otp
            )
            if len(matches) > 0:
                return True
        return False
