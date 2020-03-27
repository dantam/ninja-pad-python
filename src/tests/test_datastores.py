import json
import unittest
import datetime

from unittest.mock import (
    mock_open,
    patch,
)
from lib.configs.db_config import (
    DatastoreConfig as DC,
    DatabaseEngines as DE,
)
from lib.datastores.location_log import LocationLog
from lib.datastores.notification_log import NotificationLog
from lib.datastores.on_device_store import OnDeviceStore
from lib.datastores.contamination_log import ContaminationLog
from lib.datastores.privacy_enforcer_store import PrivacyEnforcerStore

db_config = {
    DC.ON_DEVICE_STORE: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
    DC.LOCATION_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
    DC.NOTIFICATION_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(db_config))
)
class TestDatastores(unittest.TestCase):
    def basic_test(self, log_wrapper, **entry):
        log = log_wrapper(DC('mock_file'))
        self.assertNotEqual(log, None)
        log.create()
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
        self.basic_test(NotificationLog, **entry)

    def test_on_device_store(self):
        entry = {'person_auth_id': 'pa_id'}
        self.basic_test(OnDeviceStore, **entry)

    def test_location_log(self):
        entry = {
            'encrypted_location': 'loc',
            'encrypted_otp': 'otp',
        }
        self.basic_test(LocationLog, **entry)

    def test_contamination_log(self):
        entry = {
            'encrypted_location': 'loc',
        }
        self.basic_test(ContaminationLog, **entry)

    def test_privacy_enforcer_store(self):
        entry = {
            'encrypted_location': 'loc',
            'encrypted_otp': 'otp',
        }
        self.basic_test(PrivacyEnforcerStore, **entry)

if __name__ == '__main__':
    unittest.main()
