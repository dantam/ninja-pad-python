import datetime
import sqlalchemy as db

from lib.datastores.base_datastore import BaseDatastore

class LocationLog(BaseDatastore):
    def get_table(self):
        return db.Table(
            'location_log', self.metadata,
            db.Column('time', db.DATETIME),
            db.Column('encrypted_otp', db.VARCHAR(256)),
        )

    def insert(self, time, encrypted_otp):
        query = db.insert(self.table).values(
            time=time,
            encrypted_otp=encrypted_otp
        )
        self.connection.execute(query)

    def get_where(self, times, encrypted_otp):
        return super().get_where(
            times,
            {self.table.columns.encrypted_otp: encrypted_otp}
        )

    def query(self, times=(), encrypted_otp=None):
        return super().query(self.get_where(times, encrypted_otp))

    def delete(self, times=(), encrypted_otp=None):
        return super().delete(self.get_where(times, encrypted_otp))

