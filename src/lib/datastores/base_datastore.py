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
