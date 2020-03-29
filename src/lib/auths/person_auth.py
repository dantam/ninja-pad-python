import datetime

from lib.crypto import Crypto
from lib.datastores.contamination_log import ContaminationLog
from lib.datastores.location_log import LocationLog

class PersonAuthority(Crypto):
    pass

class PersonAuthorityClient():
    def __init__(self, config):
        self.contamination_log = ContaminationLog(config)
        self.location_log = LocationLog(config)

    def upload(self, time, encrypted_otp):
        locations = self.location_log.query(
            (time - datetime.timedelta(seconds=120),
             time + datetime.timedelta(seconds=120)),
            encrypted_otp=encrypted_otp,
        )
        for location in locations:
            self.contamination_log.insert(time, location.encrypted_location)

