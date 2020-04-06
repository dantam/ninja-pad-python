import json
import random
import unittest

from unittest.mock import (
    mock_open,
    patch,
)
from lib.configs.client_config import ClientConfig

PAS = [[1], [2], [3]]
LAS = [[4], [5]]
MAS = [[6]]
PES = [[7], [8], [9], [10], [11], [12]]
config = {
    ClientConfig.PAS: PAS,
    ClientConfig.LAS: LAS,
    ClientConfig.MAS: MAS,
    ClientConfig.PES: PES,
}

@patch(
    "builtins.open",
    mock_open(read_data=json.dumps(config))
)
class TestConfig(unittest.TestCase):
    def test_get_lists(self):
        cm = ClientConfig('mock_file')
        pas = cm.get_person_auths()
        self.assertEqual(pas, PAS)

        las = cm.get_location_auths()
        self.assertEqual(las, LAS)

        mas = cm.get_medical_auths()
        self.assertEqual(mas, MAS)

        pes = cm.get_privacy_enforcers()
        self.assertEqual(pes, PES)

    @patch(
        "secrets.choice",
        side_effect=(lambda x: random.choice(x))
    )
    def test_get_item(self, mock):
        random.seed(10)
        cm = ClientConfig('mock_file')

        pa = cm.get_person_auth()
        self.assertEqual(pa, 3)

        la = cm.get_location_auth()
        self.assertEqual(la, 4)

        ma = cm.get_medical_auth()
        self.assertEqual(ma, 6)

        se = cm.get_privacy_enforcer()
        self.assertEqual(se, 10)

if __name__ == '__main__':
    unittest.main()
