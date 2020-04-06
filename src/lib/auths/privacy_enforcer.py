import json

from lib.crypto import Crypto, CryptoServer
from lib.datastores.location_log import LocationLog

class PrivacyEnforcer(Crypto):
    pass

class PrivacyEnforcerServer():
    def __init__(self, config):
        self.location_log = LocationLog(config)

    def upload(self, time, encrypted_location, encrypted_otp):
        self.location_log.insert(time, encrypted_location, encrypted_otp)

class PrivacyEnforcerClient():
    def __init__(self, privacy_enforcer_server):
        self.server = privacy_enforcer_server

    def upload(self, time, encrypted_location, encrypted_otp):
        return self.server.upload(
            time,
            encrypted_location,
            encrypted_otp,
        )

