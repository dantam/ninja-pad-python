import base64
import json

from lib.crypto import Crypto
from lib.datastores.location_log import LocationLog

class PrivacyEnforcer(Crypto):
    def __init__(self, config):
        self.location_log = LocationLog(config)
        super().__init__()

    def upload(self, time, encrypted_location, encrypted_otp):
        self.location_log.insert(time, encrypted_location, encrypted_otp)

class PrivacyEnforcerClient():
    def __init__(self, privacy_enforcer):
        self.privacy_enforcer = privacy_enforcer

    # skip security for demo
    def upload(self, time, encrypted_location, encrypted_otp):
        return self.privacy_enforcer.upload(
            time,
            encrypted_location,
            encrypted_otp,
        )

