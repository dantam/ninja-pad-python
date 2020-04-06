import datetime
import json
import tempfile
import unittest

from tempfile import NamedTemporaryFile

from unittest.mock import (
    mock_open,
    patch,
    MagicMock,
)
from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
)
from lib.datastores.location_log import LocationLog
from lib.configs.client_config import ClientConfig
from lib.clients.user_client import UserClient, round_time
from lib.crypto import CryptoClient
from lib.auths.person_auth import PersonAuthority as PA
from lib.auths.location_auth import LocationAuthorityCrypto as LAC
from lib.auths.privacy_enforcer import (
    PrivacyEnforcer as PE,
)
def setup_configs(
    person_auths,
    location_auths,
    privacy_enforcers,
    one_time_pad_length,
    public_keys_file,
    auth_type_to_auth_id_and_pem_files,
):
    sqlite_config = [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }]
    client_config = {
        ClientConfig.PAS: person_auths,
        ClientConfig.LAS: location_auths,
        ClientConfig.PES: privacy_enforcers,
        ClientConfig.ONE_TIME_PAD_LENGTH: one_time_pad_length,
        ClientConfig.PUBLIC_KEYS_FILE: public_keys_file,
        ClientConfig.ON_DEVICE_STORE: sqlite_config,
    }
    db_config = {
        DC.LOCATION_LOGS: sqlite_config,
        DC.CONTAMINATION_LOGS: sqlite_config,
        DC.NOTIFICATION_LOGS: sqlite_config,
        DC.PRIVACY_ENFORCER_STORE: sqlite_config,
    }
    public_keys_config = {}
    for auth_type, id_and_file in auth_type_to_auth_id_and_pem_files.items():
        public_keys_config[auth_type] = {
            id_and_file[0]: id_and_file[1],
        }
    return client_config, public_keys_config, db_config

def writeable_tempfile():
    return open(NamedTemporaryFile().name, 'w')

crypto_config = {
    'public_exponent': 65537,
    'key_size': 2048,
}

class TestClient(unittest.TestCase):
    def mock_user_client(self, db_config):
        return UserClient('mock_file', DC(db_config), **crypto_config)

    def simulate_env(self,
        pkeys_config,
        pem_file,
        db_config_file,
        auth,
        auth_type_to_auth_id_and_pem_files,
    ):
        client_config, public_keys_config, db_config = setup_configs(
            [1],
            [2],
            [3],
            128,
            pkeys_config.name,
            auth_type_to_auth_id_and_pem_files,
        )
        auth_pem = pem_file.name
        auth.public_key_to_file(auth_pem)
        pem_file_stream = open(auth_pem, 'rb')

        mock_client_config = 'mock_file'
        m1 = mock_open(read_data=json.dumps(client_config))
        m2 = mock_open(read_data=json.dumps(public_keys_config))
        m3 = mock_open(read_data=json.dumps(db_config))
        def mock_mapping(*args, **kargs):
            filename = args[0]
            if filename == mock_client_config:
                return m1()
            if filename == pkeys_config.name:
                return m2()
            if filename == pem_file.name:
                return pem_file_stream
            if filename == db_config_file.name:
                return m3()
        return mock_mapping

    fake_otp=b'ABCD'
    @patch(
        "secrets.token_bytes",
        return_value=fake_otp,
    )
    def test_encrypt_one_time_pad(self, mock):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file, \
                writeable_tempfile() as db_config:
            pa = PA(**crypto_config)
            mock_mapping = self.simulate_env(
                pkeys_config,
                pem_file,
                db_config,
                pa,
                {ClientConfig.PAS: (1, pem_file.name)},
            )
            with patch('builtins.open', side_effect=mock_mapping):
                client = self.mock_user_client(db_config.name)
                encrypted_otp, pa_id = client.encrypt_one_time_pad()
                otp = pa.decrypt(encrypted_otp)
            self.assertEqual(otp, TestClient.fake_otp)

    def test_encrypt_location(self):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file, \
                writeable_tempfile() as db_config:
            la = LAC(**crypto_config)
            mock_mapping = self.simulate_env(
                pkeys_config,
                pem_file,
                db_config,
                la,
                {ClientConfig.LAS: (2, pem_file.name)},
            )
            with patch('builtins.open', side_effect=mock_mapping):
                client = self.mock_user_client(db_config.name)
                location = b'abcd'
                encrypted_location = client.encrypt_location(location)
                decrypted_location = la.decrypt(encrypted_location)
                encrypted_location_2 = client.encrypt_location(location)

            self.assertEqual(location, decrypted_location)
            self.assertNotEqual(encrypted_location, encrypted_location_2)

    def test_log_location(self):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file, \
                writeable_tempfile() as db_config:
            dc = MagicMock()
            dc.get_location_logs_config = MagicMock(return_value = [{
                DC.DATABASE_ENGINE: DE.SQLITE,
                DC.DATABASE_FILE: '',
            }])
            pe = PE(dc, **crypto_config)
            mock_mapping = self.simulate_env(
                pkeys_config,
                pem_file,
                db_config,
                pe,
                {ClientConfig.PES: (3, pem_file.name)},
            )
            with patch('builtins.open', side_effect=mock_mapping):
                client = self.mock_user_client(db_config.name)
                privacy_enforcer = MagicMock()
                privacy_enforcer.upload = MagicMock(return_value=None)
                client.privacy_enforcer = privacy_enforcer
                location = b'abcd'
                time = datetime.datetime.now()
                otp = b'otp'
                client.encrypt_location = MagicMock(return_value=location)
                client.log_entry(time, location, otp)
                privacy_enforcer.upload.assert_called_with(
                    time, location, otp,
                )

    def help_test_time(self, test_time, round_seconds, expected_time):
        time = datetime.datetime.strptime(test_time, '%H:%M:%S')
        rt = round_time(time, round_seconds)
        expected_time = datetime.datetime.strptime(expected_time, '%H:%M:%S')
        self.assertEqual(rt, expected_time)

    def test_round_time(self):
        self.help_test_time('00:03:07', 1, '00:03:00')
        self.help_test_time('11:03:31', 1, '11:04:00')
        self.help_test_time('00:15:31', 15, '00:15:00')
        self.help_test_time('22:07:29', 15, '22:00:00')
        self.help_test_time('00:29:59', 60, '00:00:00')
        self.help_test_time('05:30:01', 60, '06:00:00')

if __name__ == '__main__':
    unittest.main()
