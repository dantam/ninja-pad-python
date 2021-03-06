import datetime
import sqlalchemy as db

from lib.configs.db_config import DatastoreTableNames
from lib.datastores.base_datastore import BaseDatastore

class ContaminationLog(BaseDatastore):
    def __init__(self, datastore_config, index=0):
        config = datastore_config.get_contamination_logs_config()[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            DatastoreTableNames.CONTAMINATION_LOG, self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('encrypted_location', db.TEXT),
        )
    def insert(self, time, encrypted_location):
        query = db.insert(self.table).values(
            time=time,
            encrypted_location=encrypted_location,
        )
        with self.engine.connect() as connection:
            connection.execute(query)

    def get_where(self, times, encrypted_location):
        col = self.table.columns.encrypted_location
        column_value_map = {}
        if encrypted_location is not None:
            column_value_map[col] = encrypted_location
        return super().get_where(times, column_value_map)

    def query(self, times=(), encrypted_location=None):
        return super().query(
            self.get_where(times, encrypted_location)
        )

    def delete(self, times=(), encrypted_location=None):
        return super().delete(
            self.get_where(times, encrypted_location)
        )

