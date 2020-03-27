import json
import tempfile
import unittest

from tempfile import NamedTemporaryFile

from unittest.mock import (
    mock_open,
    patch,
)
from lib.configs.client_config import ClientConfig
from lib.client import Client
from lib.person_auth import PersonAuthority as PA
from lib.location_auth import LocationAuthority as LA

def setup_configs(
    person_auths,
    location_auths,
    security_enforcers,
    token_length,
    public_keys_file,
    auth_type_to_auth_id_and_pem_files,
):
    client_config = {
        ClientConfig.PAS: person_auths,
        ClientConfig.LAS: location_auths,
        ClientConfig.SES: security_enforcers,
        ClientConfig.TOKEN_LENGTH: token_length,
        ClientConfig.PUBLIC_KEYS_FILE: public_keys_file,
    }
    public_keys_config = {}
    for auth_type, id_and_file in auth_type_to_auth_id_and_pem_files.items():
        public_keys_config[auth_type] = {
            id_and_file[0]: id_and_file[1],
        }
    return client_config, public_keys_config

def writeable_tempfile():
    return open(NamedTemporaryFile().name, 'w')

class TestClient(unittest.TestCase):
    def simulate_env(self,
        pkeys_config,
        pem_file,
        auth,
        auth_type_to_auth_id_and_pem_files,
    ):
        client_config, public_keys_config = setup_configs(
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
        def mock_mapping(*args, **kargs):
            if args[0] == mock_client_config:
                return m1()
            if args[0] == pkeys_config.name:
                return m2()
            if args[0] == pem_file.name:
                return pem_file_stream
        return mock_mapping

    fake_otp='ABCD'
    @patch(
        "secrets.token_hex",
        return_value=fake_otp,
    )
    def test_encrypt_one_time_pad(self, mock):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file:
            pa = PA()
            mock_mapping = self.simulate_env(
                pkeys_config,
                pem_file,
                pa,
                {ClientConfig.PAS: (1, pem_file.name)},
            )
            with patch('builtins.open', side_effect=mock_mapping):
                client = Client('mock_file')
                encrypted_otp = client.encrypt_one_time_pad()
                otp = pa.decrypt(encrypted_otp)
            self.assertEqual(otp, TestClient.fake_otp.encode())

    def test_encrypt_location(self):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file:
            la = LA()
            mock_mapping = self.simulate_env(
                pkeys_config,
                pem_file,
                la,
                {ClientConfig.LAS: (2, pem_file.name)},
            )
            with patch('builtins.open', side_effect=mock_mapping):
                client = Client('mock_file')
                location = b'abcd'
                encrypted_location = client.encrypt_location(location)
                decrypted_location = la.decrypt(encrypted_location)
                encrypted_location_2 = client.encrypt_location(location)

            self.assertEqual(location, decrypted_location)
            self.assertNotEqual(encrypted_location, encrypted_location_2)


    def test_log_location(self):
        pass

if __name__ == '__main__':
    unittest.main()
