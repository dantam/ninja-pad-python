from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
)

class Crypto:
    padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    def __init__(self, **kwargs):
        self.private_key = rsa.generate_private_key(
            backend=default_backend(),
            public_exponent=kwargs['public_exponent'],
            key_size=kwargs['key_size'],
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext):
        return self.public_key.encrypt(
            plaintext,
            Crypto.padding,
        )

    def decrypt(self, ciphertext):
        return self.private_key.decrypt(
            ciphertext,
            Crypto.padding,
        )

    def public_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def public_key_to_file(self, filename):
        payload = self.public_bytes()
        with open(filename, 'wb') as f:
            f.write(payload)

    def UNSAFE_private_key_to_file(self, filename):
        payload = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(filename, 'wb') as f:
            f.write(payload)

class CryptoClient:
    def __init__(self, filename):
        self.public_key = self.public_key_from_file(filename)

    def public_key_from_file(self, filename):
        with open(filename, "rb") as f:
            return serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )

    def encrypt(self, val):
        return self.public_key.encrypt(
            val,
            padding=Crypto.padding,
        )

    def public_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

class CryptoServer:
    def __init__(self, filename):
        self.private_key = self.private_key_from_file(filename)

    def private_key_from_file(self, filename):
        with open(filename, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

    def encrypt(self, val):
        return self.private_key.encrypt(
            val,
            padding=Crypto.padding,
        )

    def decrypt(self, val):
        return self.private_key.decrypt(
            val,
            padding=Crypto.padding,
        )
