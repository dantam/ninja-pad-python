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
            db.Column('salted_otp', db.VARCHAR(256)),
        )

    def insert(self, time, salted_otp, person_auth_id):
        query = db.insert(self.table).values(
            time=time,
            salted_otp=salted_otp,
            person_auth_id=person_auth_id
        )
        with self.engine.connect() as connection:
            return connection.execute(query)

    def get_where(self, times, salted_otp, person_auth_id):
        column_value_map = {}
        col = self.table.columns.salted_otp
        if salted_otp is not None:
            column_value_map[col] = salted_otp
        col = self.table.columns.person_auth_id
        if person_auth_id is not None:
            column_value_map[col] = person_auth_id

        return super().get_where(
            times,
            column_value_map,
        )

    def query(self, times=(), salted_otp=None, person_auth_id=None):
        return super().query(self.get_where(times, salted_otp, person_auth_id))

    def delete(self, times=(), salted_otp=None, person_auth_id=None):
        return super().delete(self.get_where(times, salted_otp, person_auth_id))

    def get_since(self, personal_auth_id, start_time):
        clauses = [
            self.table.columns.person_auth_id == personal_auth_id,
            self.table.columns.time >= start_time
        ]
        return super().query(db.and_(*clauses))


