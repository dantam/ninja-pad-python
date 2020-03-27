import datetime
import sqlalchemy as db

from lib.datastores.base_datastore import BaseDatastore

class OnDeviceStore(BaseDatastore):
    def __init__(self, datastore_config, index=0):
        config = datastore_config.get_on_device_store_config()[index]
        super().__init__(config)

    def get_table(self):
        return db.Table(
            'on_device_store', self.metadata,
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
        self.connection.execute(query)

    def get_where(self, times, salted_otp, person_auth_id):
        return super().get_where(
            times,
            {self.table.columns.person_auth_id: person_auth_id}
        )

    def query(self, times=(), salted_otp=None, person_auth_id=None):
        return super().query(self.get_where(times, salted_otp, person_auth_id))

    def delete(self, times=(), salted_otp=None, person_auth_id=None):
        return super().delete(self.get_where(times, salted_otp, person_auth_id))
