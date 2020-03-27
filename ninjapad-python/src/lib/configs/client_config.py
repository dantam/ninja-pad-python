import json
import secrets

class ClientConfig:
    PAS = 'personal_authorities'
    LAS = 'location_authorities'
    MAS = 'medical_authorities'
    SES = 'security_enforcers'
    TOKEN_LENGTH = 'token_length'

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
        return self.get_random_value(ClientConfig.PAS)

    def get_location_auths(self):
        return self.get_value(ClientConfig.LAS)

    def get_location_auth(self):
        return self.get_random_value(ClientConfig.LAS)

    def get_medical_auths(self):
        return self.get_value(ClientConfig.MAS)

    def get_medical_auth(self):
        return self.get_random_value(ClientConfig.MAS)

    def get_security_enforcers(self):
        return self.get_value(ClientConfig.SES)

    def get_security_enforcer(self):
        return self.get_random_value(ClientConfig.SES)

    def get_token_len(self):
        return self.get_value(ClientConfig.TOKEN_LENGTH)

