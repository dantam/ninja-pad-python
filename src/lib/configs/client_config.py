import json
import secrets

class ClientConfig:
    PAS = 'personal_authorities'
    LAS = 'location_authorities'
    MAS = 'medical_authorities'
    PES = 'privacy_enforcers'
    ONE_TIME_PAD_LENGTH = 'one_time_pad_length'
    PUBLIC_KEYS_FILE = 'public_keys_file'
    ON_DEVICE_STORE = 'on_device_store'

    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)

    def get_value(self, key):
        return self.config[key]

    def get_random_value(self, key):
        return secrets.choice(self.get_value(key))

    def get_person_auths(self):
        return self.get_value(ClientConfig.PAS)

    def get_person_auth(self):
        return self.get_random_value(ClientConfig.PAS)[0]

    def get_location_auths(self):
        return self.get_value(ClientConfig.LAS)

    def get_location_auth(self):
        return self.get_random_value(ClientConfig.LAS)[0]

    def get_medical_auths(self):
        return self.get_value(ClientConfig.MAS)

    def get_medical_auth(self):
        return self.get_random_value(ClientConfig.MAS)[0]

    def get_privacy_enforcers(self):
        return self.get_value(ClientConfig.PES)

    def get_privacy_enforcer(self):
        return self.get_random_value(ClientConfig.PES)[0]

    def get_one_time_pad_length(self):
        return int(self.get_value(ClientConfig.ONE_TIME_PAD_LENGTH))

    def get_public_keys_file(self):
        return self.get_value(ClientConfig.PUBLIC_KEYS_FILE)

    def get_on_device_config(self):
        return self.get_value(ClientConfig.ON_DEVICE_STORE)

