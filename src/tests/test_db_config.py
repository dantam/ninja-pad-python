import json
import random
import unittest

from unittest.mock import (
    mock_open,
    patch,
)
from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
)

TEST_ENGINE_MYSQL = 'mysql'
TEST_ENGINE_NONE = 'none'
TEST_DATABASE_NAME_1 = 'name_1'
TEST_DATABASE_NAME_2 = 'name_2'
TEST_DATABASE_USER = 'user'
TEST_DATABASE_PASSWORD = 'password'
TEST_DATABASE_HOST = 'host'
TEST_DATABASE_PORT = 'port'

db_config = {
    DC.LOCATION_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_1,
        DC.DATABASE_USER: TEST_DATABASE_USER,
        DC.DATABASE_PASSWORD: TEST_DATABASE_PASSWORD,
        DC.DATABASE_HOST: TEST_DATABASE_HOST,
        DC.DATABASE_PORT: TEST_DATABASE_PORT,
    }],
    DC.CONTAMINATION_LOGS: [{
        DC.DATABASE_ENGINE: TEST_ENGINE_NONE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_2,
        DC.DATABASE_USER: TEST_DATABASE_USER,
    }],
    DC.NOTIFICATION_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_1,
        DC.DATABASE_USER: TEST_DATABASE_USER,
    }, {
        DC.DATABASE_ENGINE: TEST_ENGINE_NONE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_2,
        DC.DATABASE_USER: TEST_DATABASE_USER,
    }],
    DC.PRIVACY_ENFORCER_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_1,
        DC.DATABASE_USER: TEST_DATABASE_USER,
        DC.DATABASE_PASSWORD: TEST_DATABASE_PASSWORD,
        DC.DATABASE_HOST: TEST_DATABASE_HOST,
        DC.DATABASE_PORT: TEST_DATABASE_PORT,
    }],
    DC.ON_DEVICE_STORE: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_NAME: TEST_DATABASE_NAME_1,
    }],
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(db_config))
)
class TestDatastoreConfig(unittest.TestCase):
    def test_get_logs_config(self):
        dc = DC('mock_file')
        test_pairs = [
            (DC.LOCATION_LOGS, dc.get_location_logs_config),
            (DC.NOTIFICATION_LOGS, dc.get_notification_logs_config),
            (DC.CONTAMINATION_LOGS, dc.get_contamination_logs_config),
            (DC.PRIVACY_ENFORCER_LOGS, dc.get_privacy_enforcer_logs_config),
            (DC.ON_DEVICE_STORE, dc.get_on_device_store_config),
        ]
        for test_pair in test_pairs:
            config = test_pair[1]()
            self.assertEqual(config, db_config[test_pair[0]])

if __name__ == '__main__':
    unittest.main()
