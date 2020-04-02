import datetime
import sqlalchemy as db

from lib.configs.db_config import DatastoreTableNames
from lib.datastores.base_location_log import BaseLocationLog

class LocationLog(BaseLocationLog):
    def __init__(self, datastore_config, index=0):
        config = datastore_config.get_location_logs_config()[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            DatastoreTableNames.LOCATION_LOG, self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('encrypted_location', db.TEXT),
            db.Column('encrypted_otp', db.TEXT),
        )

