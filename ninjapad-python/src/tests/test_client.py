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

def setup_configs(
    person_auths,
    location_auths,
    security_enforcers,
    token_length,
    public_keys_file,
    public_key_file,
):
    client_config = {
        ClientConfig.PAS: person_auths,
        ClientConfig.LAS: location_auths,
        ClientConfig.SES: security_enforcers,
        ClientConfig.TOKEN_LENGTH: token_length,
        ClientConfig.PUBLIC_KEYS_FILE: public_keys_file,
    }
    public_keys_config = {
        ClientConfig.PAS: {
            1: public_key_file,
        },
    }
    return client_config, public_keys_config

def writeable_tempfile():
    return open(NamedTemporaryFile().name, 'w')

class TestClient(unittest.TestCase):
    fake_otp='ABCD'
    @patch(
        "secrets.token_hex",
        return_value=fake_otp,
    )
    def test_encrypt_one_time_pad(self, mock):
        with writeable_tempfile() as pkeys_config, \
                writeable_tempfile() as pem_file:
            client_config, public_keys_config = setup_configs(
                [1],
                [2],
                [3],
                128,
                pkeys_config.name,
                pem_file.name,
            )
            pa = PA()
            pa_pem = pem_file.name
            pa.public_key_to_file(pa_pem)
            pem_file_stream = open(pa_pem, 'rb')

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
            with patch('builtins.open', side_effect=mock_mapping):
                client = Client('mock_file')
                encrypted_otp = client.encrypt_one_time_pad()
                otp = pa.decrypt(encrypted_otp)
            self.assertEqual(otp, TestClient.fake_otp.encode())

    def test_encrypt_location(self):
        pass

    def test_log_location(self):
        pass

if __name__ == '__main__':
    unittest.main()
