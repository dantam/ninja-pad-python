import base64
import json

from lib.crypto import Crypto

class PrivacyEnforcer(Crypto):
    pass

def bytes_to_string(b):
    return base64.b64encode(b).decode('ascii')

def json_to_bytes(j):
    return json.dumps(j).encode()

def make_payload(time, loc, otp):
    return {
        'time': time,
        'encrypted_location': bytes_to_string(loc),
        'encrypted_otp': bytes_to_string(otp),
    }

class PrivacyEnforcerClient():
    def __init__(self, crypto_client):
        self.crypto_client = crypto_client

    def encrypt(self, time, encrypted_location, encrypted_otp):
        payload = make_payload(time, encrypted_location, encrypted_otp)
        return self.crypto_client.encrypt(json_to_bytes(payload))

