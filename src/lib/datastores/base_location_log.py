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
        with self.engine.connect() as connection:
            connection.execute(query)

    def get_where(self, times, encrypted_location, encrypted_otp):
        cols = self.table.columns
        column_value_map = {}
        if encrypted_location is not None:
            column_value_map[cols.encrypted_location] = encrypted_location
        if encrypted_otp is not None:
            column_value_map[cols.encrypted_otp] = encrypted_otp
        return super().get_where(times, column_value_map)

    def query(self, times=(), **kwargs):
        encrypted_location = kwargs.get('encrypted_location', None)
        encrypted_otp = kwargs.get('encrypted_otp', None)
        return super().query(
            self.get_where(times, encrypted_location, encrypted_otp)
        )

    def delete(self, times=(), encrypted_location=None, encrypted_otp=None):
        return super().delete(
            self.get_where(times, encrypted_location, encrypted_otp)
        )
