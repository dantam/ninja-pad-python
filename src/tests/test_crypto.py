import unittest
import random
import tempfile

from cryptography.hazmat.primitives import (
    serialization,
)
from lib.crypto import (
    Crypto,
    CryptoClient,
)

class TestCrypto(unittest.TestCase):
    def setup(self):
        random.seed(0)

    def test_encrypt_decrypt(self):
        crypto = Crypto(public_exponent=65537, key_size=2048)
        plain = b'test'
        cipher = crypto.encrypt(plain)
        output = crypto.decrypt(cipher)
        self.assertEqual(plain, output)

    def test_public_key_serializeation(self):
        crypto = Crypto(public_exponent=65537, key_size=2048)
        with open(tempfile.NamedTemporaryFile().name, 'w') as f:
            crypto.public_key_to_file(f.name)
            crypto_client = CryptoClient(f.name)

        self.assertEqual(
            crypto.public_bytes(),
            crypto_client.public_bytes(),
        )

if __name__ == '__main__':
    unittest.main()
