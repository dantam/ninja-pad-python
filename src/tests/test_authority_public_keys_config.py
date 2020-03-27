import json
import random
import unittest

from unittest.mock import (
    mock_open,
    patch,
)
from lib.auths.person_auth import PersonAuthority as PA
from lib.configs.client_config import ClientConfig
from lib.configs.authority_public_keys_config import (
    AuthorityPublicKeysConfig as APKC,
)

PUBLIC_KEY_1 = 'ABC'
PUBLIC_KEY_2 = 'DEF'
public_keys = {
    ClientConfig.PAS: {
        1: PUBLIC_KEY_1,
        2: PUBLIC_KEY_2,
    },
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(public_keys))
)
class TestAuthorityPublicKeys(unittest.TestCase):
    def test_get_public_key_value(self):
        pkey_config = APKC('mock_file')
        pas = pkey_config.get_public_key_value(
            ClientConfig.PAS,
            '2',
        )
        self.assertEqual(pas, PUBLIC_KEY_2)

if __name__ == '__main__':
    unittest.main()
