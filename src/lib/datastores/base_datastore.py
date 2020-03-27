import datetime
import sqlalchemy as db

from lib.configs.db_config import ConfigFactory

class BaseDatastore:
    def __init__(self, datastore_config, index=0):
        entries = datastore_config.get_on_device_store_config()
        self.config = ConfigFactory.get(entries[index])
        self.engine = db.create_engine(self.config.get_create_engine())
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.get_table()
        self.create()

    def create(self):
        self.metadata.create_all(self.engine)

    def get_time_range(
        self,
        end=datetime.datetime.now(),
        delta=datetime.timedelta(days=28),
    ):
        return (end-delta, end)

    def get_where(self, times, column_value_map):
        if len(times) == 0:
            times = self.get_time_range()
        clauses = [
            self.table.columns.time >= times[0],
            self.table.columns.time <= times[1],
        ]
        for column, value in column_value_map.items():
            clauses.append(column == value)
        return db.and_(*clauses)

    def query(self, where_clause):
        query = db.select([self.table]).where(where_clause)
        return self.connection.execute(query).fetchall()

    def delete(self, where_clause):
        query = self.table.delete().where(where_clause)
        return self.connection.execute(query)

