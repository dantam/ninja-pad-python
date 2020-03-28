from lib.crypto import Crypto
from lib.datastores.contamination_log import ContaminationLog

class PersonAuthority(Crypto):
    pass

class PersonAuthorityClient():
    def __init__(self, config):
        self.contamination_log = ContaminationLog(config)

    def upload(self, time, encrypted_otp):
        self.contamination_log.insert(time, encrypted_otp)

