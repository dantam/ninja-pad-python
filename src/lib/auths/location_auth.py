import datetime

from lib.configs.client_config import ClientConfig
from lib.crypto import (
    Crypto,
    CryptoServer,
)
from lib.configs.authority_public_keys_config import (
    AuthorityPublicKeysConfig as APKC,
)
from lib.datastores.contamination_log import ContaminationLog
from lib.datastores.notification_log import NotificationLog
from lib.datastores.location_log import LocationLog

class LocationAuthorityCrypto(Crypto):
    pass

class LocationAuthorityClient():
    pass

class LocationAuthority():
    def __init__(self, auth_id, client_config, db_config, private_key_file):
        self.auth_id = auth_id
        self.contamination_log = ContaminationLog(db_config)
        self.notification_log = NotificationLog(db_config)
        self.location_log = LocationLog(db_config)
        self.crypto_server = CryptoServer(private_key_file)
        self.setup_other_location_auths(client_config)

    def setup_other_location_auths(self, client_config):
        client_config = ClientConfig(client_config)
        self.public_keys_config = APKC(
            client_config.get_public_keys_file()
        )
        auth_type = ClientConfig.LAS
        auth_ids = self.public_keys_config.get_public_auth_ids(auth_type)
        self.other_las = {}
        for auth_id in auth_ids:
            if int(auth_id) == self.auth_id:
                continue
            self.other_las[auth_id] = self.public_keys_config.get_public_key(
                auth_type,
                auth_id,
            )

    def get_contaminations(self, start_time, end_time):
        results = self.contamination_log.query((start_time, end_time))
        my_results = []
        for result in results:
            try:
                dec = self.crypto_server.decrypt(result.encrypted_location)
                if not dec:
                    print('no dec')
                    continue
                my_results.append((dec, result))
            except ValueError:
                print('location auth decrypt fail')
        return my_results

    def process_contaminations(self, start_time, end_time):
        my_results = self.get_contaminations(start_time, end_time)
        self.publish_to_other_location_auths(my_results)
        self.find_and_publish_encrypted_otps(my_results)

    def publish_to_other_location_auths(self, my_results):
        for r in my_results:
            data = r[1]
            matches = self.location_log.query(
                (data.time - datetime.timedelta(seconds=120),
                 data.time + datetime.timedelta(seconds=120)),
                encrypted_location=data.encrypted_location,
            )
            for m in matches:
                self.notification_log.insert(data.time, m.encrypted_otp)

    def find_and_publish_encrypted_otps(self, my_results):
        for la in self.other_las.values():
            for r in my_results:
                location = r[0]
                encrypted_location = la.encrypt(location)
                data = r[1]
                self.contamination_log.insert(
                    data.time,
                    encrypted_location,
                )
