import json

from lib.crypto import Crypto
from lib.datastores.location_log import LocationLog

from lib.auths.person_auth import (
    PersonAuthorityClient,
)
class MedicalAuthority(Crypto):
    pass

class MedicalAuthorityClient():
    def __init__(self, db_config):
        self.person_auth_client = PersonAuthorityClient(db_config)

    # skip security for demo
    def upload(self, payload):
        self.person_auth_client.upload(payload)
