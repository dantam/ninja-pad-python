import datetime
import sqlalchemy as db

from lib.datastores.base_datastore import BaseDatastore

class OnDeviceStore(BaseDatastore):
    def get_table(self):
        return db.Table(
            'on_device_store', self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('person_auth_id', db.INTEGER),
        )

    def insert(self, time, person_auth_id):
        query = db.insert(self.table).values(
            time=time,
            person_auth_id=person_auth_id
        )
        self.connection.execute(query)

    def get_where(self, times, person_auth_id):
        return super().get_where(
            times,
            {self.table.columns.person_auth_id: person_auth_id}
        )

    def query(self, times=(), person_auth_id=None):
        return super().query(self.get_where(times, person_auth_id))

    def delete(self, times=(), person_auth_id=None):
        return super().delete(self.get_where(times, person_auth_id))
