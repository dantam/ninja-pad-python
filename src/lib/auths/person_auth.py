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

    def upload(self, payload):
        contaminations = []
        for entry in payload:
            time = entry.time
            locations = self.location_log.query(
                (time - datetime.timedelta(seconds=120),
                 time + datetime.timedelta(seconds=120)),
                encrypted_otp=entry.encrypted_otp,
            )
            contaminations += locations
        for contamination in contaminations:
            self.contamination_log.insert(
                contamination.time,
                contamination.encrypted_location
            )

