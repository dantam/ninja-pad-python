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

    def create(self):
        self.metadata.create_all(self.engine)

    def insert(self, time, encrypted_otp):
        query = db.insert(self.table).values(
            time=time,
            encrypted_otp=encrypted_otp
        )
        self.connection.execute(query)

    def get_time_range(
        self,
        end=datetime.datetime.now(),
        delta=datetime.timedelta(days=28),
    ):
        return (end-delta, end)

    def get_where(self, times, encrypted_otp):
        if len(times) == 0:
            times = self.get_time_range()
        clauses = [
            self.table.columns.time >= times[0],
            self.table.columns.time <= times[1],
        ]
        if encrypted_otp != None:
            clauses.append(
                self.table.columns.encrypted_otp == encrypted_otp
            )
        return db.and_(*clauses)

    def query(self, times=(), encrypted_otp=None):
        query = db.select([self.table]).where(
            self.get_where(times, encrypted_otp)
        )
        return self.connection.execute(query).fetchall()

    def delete(self, times=(), encrypted_otp=None):
        query = self.table.delete().where(
            self.get_where(times, encrypted_otp)
        )
        return self.connection.execute(query)

