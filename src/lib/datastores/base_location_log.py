import datetime
import sqlalchemy as db

from lib.configs.db_config import ConfigFactory
from lib.datastores.base_datastore import BaseDatastore

class BaseLocationLog(BaseDatastore):
    def insert(self, time, encrypted_location, encrypted_otp):
        query = db.insert(self.table).values(
            time=time,
            encrypted_location=encrypted_location,
            encrypted_otp=encrypted_otp
        )
        self.connection.execute(query)

    def get_where(self, times, encrypted_location, encrypted_otp):
        column_value_map = {
            self.table.columns.encrypted_location: encrypted_location,
            self.table.columns.encrypted_otp: encrypted_otp,
        }
        return super().get_where(times, column_value_map)

    def query(self, times=(), encrypted_location=None, encrypted_otp=None):
        return super().query(
            self.get_where(times, encrypted_location, encrypted_otp)
        )

    def delete(self, times=(), encrypted_location=None, encrypted_otp=None):
        return super().delete(
            self.get_where(times, encrypted_location, encrypted_otp)
        )
