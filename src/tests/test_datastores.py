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
from lib.datastores.on_device_store import OnDeviceStore

db_config = {
    DC.ON_DEVICE_STORE: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
    DC.LOCATION_LOGS: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(db_config))
)
class TestDatastores(unittest.TestCase):
    def basic_test(self, log):
        dc = DC('mock_file')
        log = LocationLog(dc)
        self.assertNotEqual(log, None)
        log.create()
        rs = log.query()
        self.assertEqual(rs, [])
        now = datetime.datetime.now()
        early = now - datetime.timedelta(minutes=1)
        earlier = now - datetime.timedelta(minutes=2)
        data = 'abc'
        rs = log.insert(early, data)
        rs = log.query((earlier, now), data)
        self.assertEqual(rs, [(early, data)])
        rs = log.delete((), data)
        rs = log.query((earlier, now), data)
        self.assertEqual(rs, [])

    def test_location_log(self):
        self.basic_test(
            LocationLog(DC('mock_file')),
        )
    def test_on_device_store(self):
        self.basic_test(
            OnDeviceStore(DC('mock_file'))
        )

if __name__ == '__main__':
    unittest.main()
