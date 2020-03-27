import unittest
import random

from lib.crypto import Crypto

class TestCrypto(unittest.TestCase):
    def setup(self):
        random.seed(0)

    def test_encrypt_decrypt(self):
        crypto = Crypto()
        plain = b'test'
        cipher = crypto.encrypt(plain)
        output = crypto.decrypt(cipher)
        self.assertEqual(plain, output)

if __name__ == '__main__':
    unittest.main()
