import json
import os
import secrets

class DatabaseEngines:
    SQLITE = 'sqlite3'

class ConfigMissingException(Exception):
    pass

class BaseDatastoreConfig:
    DATABASE_ENGINE = "database_engine"
    DATABASE_NAME = "database_name"
    DATABASE_USER = "database_user"
    DATABASE_PASSWORD = "database_password"
    DATABASE_HOST = "database_host"
    DATABASE_PORT = "database_port"
    DATABASE_FILE = "database_file"

    def __init__(self, config):
        self.config = config

    def get_value(self, key):
        return self.config.get(key, None)

    def must_get_value(self, key):
        value = self.get_value(key)
        if value == None:
            raise ConfigMissingException('Config Missing: {}'.format(key))
        return value

class DatastoreConfig(BaseDatastoreConfig):
    LOCATION_LOGS = 'location_logs'
    CONTAMINATION_LOGS = 'contamination_logs'
    NOTIFICATION_LOGS = 'notification_logs'
    PRIVACY_ENFORCER_STORE = 'privacy_enforcer_store'
    ON_DEVICE_STORE = "on_device_store"

    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)

    def get_location_logs_config(self):
        return self.must_get_value(DatastoreConfig.LOCATION_LOGS)

    def get_contamination_logs_config(self):
        return self.must_get_value(DatastoreConfig.CONTAMINATION_LOGS)

    def get_notification_logs_config(self):
        return self.must_get_value(DatastoreConfig.NOTIFICATION_LOGS)

    def get_privacy_enforcer_store_config(self):
        return self.must_get_value(DatastoreConfig.PRIVACY_ENFORCER_STORE)

    def get_on_device_store_config(self):
        return self.must_get_value(DatastoreConfig.ON_DEVICE_STORE)

class UnsupportedDatabaseEngineException(Exception):
    pass

class ConfigFactory():
    def get(config):
        engine = config.get(DatastoreConfig.DATABASE_ENGINE)
        if engine == DatabaseEngines.SQLITE:
            return SQLiteConfig(config)
        msg = 'Unsupported engine: {}'.format(engine)
        raise UnsupportedDatabaseEngineException(msg)

class SQLiteConfig(BaseDatastoreConfig):
    def __init__(self, config):
        self.config = config

    def get_create_engine(self):
        fullpath = self.config.get(BaseDatastoreConfig.DATABASE_FILE, '')
        if fullpath != '':
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        return 'sqlite://{}/{}'.format(
            self.config.get(BaseDatastoreConfig.DATABASE_HOST, ''),
            fullpath,
         )

class DatastoreTableNames:
    LOCATION_LOG = 'location_log'
    CONTAMINATION_LOG = 'contamination_log'
    NOTIFICATION_LOG = 'notification_log'
    PRIVACY_ENFORCER_STORE = 'privacy_enforcer_store'
    ON_DEVICE_STORE = "on_device_store"

