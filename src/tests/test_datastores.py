import json
import unittest
import datetime

from unittest.mock import (
    mock_open,
    patch,
)
from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatastoreTableNames as Table,
    DatabaseEngines as DE,
    ConfigMissingException,
)
from lib.datastores.location_log import LocationLog
from lib.datastores.notification_log import NotificationLog
from lib.datastores.on_device_store import OnDeviceStore
from lib.datastores.contamination_log import ContaminationLog
from lib.datastores.privacy_enforcer_store import PrivacyEnforcerStore

test_config = [{
    DC.DATABASE_ENGINE: DE.SQLITE,
    DC.DATABASE_FILE: '',
}]
stores = [
    DC.ON_DEVICE_STORE,
    DC.LOCATION_LOGS,
    DC.NOTIFICATION_LOGS,
    DC.CONTAMINATION_LOGS,
    DC.PRIVACY_ENFORCER_STORE,
]
db_config = {k: test_config for k in stores}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(db_config))
)
class TestDatastores(unittest.TestCase):
    def basic_test(self, db_wrapper, table_name, **entry):
        log = db_wrapper(DC('mock_file'))
        self.assertNotEqual(log, None)
        log.create()
        self.assertEqual(log.table.name, table_name)
        rs = log.query()
        self.assertEqual(rs, [])
        now = datetime.datetime.now()
        early = now - datetime.timedelta(minutes=1)
        earlier = now - datetime.timedelta(minutes=2)
        rs = log.insert(early, **entry)
        rs = log.query((earlier, now), **entry)
        expected = tuple([early] + [v for v in entry.values()])
        self.assertEqual(rs, [expected])
        rs = log.delete((), **entry)
        rs = log.query((earlier, now), **entry)
        self.assertEqual(rs, [])

    def test_notification_log(self):
        entry = {'encrypted_otp': 'otp'}
        self.basic_test(NotificationLog, Table.NOTIFICATION_LOG, **entry)

    def test_on_device_store(self):
        entry = {
            'person_auth_id': 'pa_id',
            'salted_otp': 'salted_otp',
         }
        self.basic_test(OnDeviceStore, Table.ON_DEVICE_STORE, **entry)

    def test_location_log(self):
        entry = {
            'encrypted_location': 'loc',
            'encrypted_otp': 'otp',
        }
        self.basic_test(LocationLog, Table.LOCATION_LOG, **entry)

    def test_contamination_log(self):
        entry = {
            'encrypted_location': 'loc',
        }
        self.basic_test(ContaminationLog, Table.CONTAMINATION_LOG, **entry)

    def test_privacy_enforcer_store(self):
        entry = {
            'encrypted_location': 'loc',
            'encrypted_otp': 'otp',
        }
        self.basic_test(
            PrivacyEnforcerStore,
            Table.PRIVACY_ENFORCER_STORE,
            **entry
        )

    def test_missing_log_config(self):
        entry = {
            'encrypted_location': 'loc',
            'encrypted_otp': 'otp',
        }
        config = db_config
        del(config[DC.PRIVACY_ENFORCER_STORE])
        with patch('builtins.open', mock_open(read_data=json.dumps(config))), \
            self.assertRaises(ConfigMissingException):
                self.basic_test(
                    PrivacyEnforcerStore,
                    Table.PRIVACY_ENFORCER_STORE,
                    **entry
                )

if __name__ == '__main__':
    unittest.main()
