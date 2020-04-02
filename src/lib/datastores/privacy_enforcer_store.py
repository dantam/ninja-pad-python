import sqlalchemy as db

from lib.configs.db_config import DatastoreTableNames
from lib.datastores.base_location_log import BaseLocationLog

class PrivacyEnforcerStore(BaseLocationLog):
    def __init__(self, datastore_config, index=0):
        config = datastore_config.get_privacy_enforcer_store_config()[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            DatastoreTableNames.PRIVACY_ENFORCER_STORE, self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('encrypted_location', db.TEXT),
            db.Column('encrypted_otp', db.TEXT),
        )

