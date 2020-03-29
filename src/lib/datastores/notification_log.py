import datetime
import sqlalchemy as db

from lib.configs.db_config import DatastoreTableNames
from lib.datastores.base_datastore import BaseDatastore

class NotificationLog(BaseDatastore):
    def __init__(self, datastore_config, index=0):
        config = datastore_config.get_notification_logs_config()[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            DatastoreTableNames.NOTIFICATION_LOG, self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('encrypted_otp', db.VARCHAR(256)),
        )

    def insert(self, time, encrypted_otp):
        query = db.insert(self.table).values(
            time=time,
            encrypted_otp=encrypted_otp
        )
        with self.engine.connect() as connection:
            connection.execute(query)

    def get_where(self, times, encrypted_otp):
        col = self.table.columns.encrypted_otp
        column_value_map = {}
        if encrypted_otp is not None:
            column_value_map[col] = encrypted_otp
        return super().get_where(
            times,
            column_value_map,
        )

    def query(self, times=(), encrypted_otp=None):
        return super().query(self.get_where(times, encrypted_otp))

    def delete(self, times=(), encrypted_otp=None):
        return super().delete(self.get_where(times, encrypted_otp))


