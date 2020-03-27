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

db_config = {
    DC.ON_DEVICE_STORE: [{
        DC.DATABASE_ENGINE: DE.SQLITE,
        DC.DATABASE_FILE: '',
    }],
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(db_config))
)
class TestDatastores(unittest.TestCase):
    def test_location_log(self):
        dc = DC('mock_file')
        log = LocationLog(dc)
        self.assertNotEqual(log, None)
        log.create()
        rs = log.query()
        self.assertEqual(rs, [])
        now = datetime.datetime.now()
        early = now - datetime.timedelta(minutes=1)
        earlier = now - datetime.timedelta(minutes=2)
        otp = 'abc'
        rs = log.insert(early, otp)
        rs = log.query((earlier, now), otp)
        self.assertEqual(rs, [(early, otp)])
        rs = log.delete((), otp)
        rs = log.query((earlier, now), otp)
        self.assertEqual(rs, [])

if __name__ == '__main__':
    unittest.main()
