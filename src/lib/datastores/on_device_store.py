import datetime
import sqlalchemy as db

from lib.configs.db_config import DatastoreTableNames
from lib.datastores.base_datastore import BaseDatastore

class OnDeviceStore(BaseDatastore):
    def __init__(self, datastore_config, index=0):
        config = datastore_config[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            DatastoreTableNames.ON_DEVICE_STORE, self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('person_auth_id', db.INTEGER),
            db.Column('encrypted_otp', db.TEXT),
        )

    def insert(self, time, encrypted_otp, person_auth_id):
        query = db.insert(self.table).values(
            time=time,
            encrypted_otp=encrypted_otp,
            person_auth_id=person_auth_id
        )
        with self.engine.connect() as connection:
            return connection.execute(query)

    def get_where(self, times, **kwargs):
        column_value_map = {}
        cols = self.table.columns
        encrypted_otp = kwargs.get('encrypted_otp')
        person_auth_id = kwargs.get('person_auth_id')
        if encrypted_otp:
            column_value_map[cols.encrypted_otp] = encrypted_otp
        if person_auth_id:
            column_value_map[cols.person_auth_id] = person_auth_id

        return super().get_where(
            times,
            column_value_map,
        )

    def query(self, times=(), **kwargs):
        return super().query(self.get_where(times, **kwargs))

    def delete(self, times=(), **kwargs):
        return super().delete(self.get_where(times, **kwargs))

    def get_since(self, personal_auth_id, start_time):
        clauses = [
            self.table.columns.person_auth_id == personal_auth_id,
            self.table.columns.time >= start_time
        ]
        return super().query(db.and_(*clauses))


