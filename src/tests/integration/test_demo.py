import json
import unittest
import datetime
import numpy as np

from collections import defaultdict
from demo.driver import drive
from demo.runenv import brownian
from demo.shared_params import defaults as params

from unittest.mock import patch

collision_xpos = np.array([
    [3,  8,  8,  7,  9,  8,  7,  1,  1,  7,  2,  3, 10,  4,  8,  3,
     4,  7,  1,  5,  8,  6,  1,  9,  3],
    [3,  3,  4,  1,  5,  8,  7,  9,  3,  8,  6,  8,  6,  1,  6,  3,
     9,  0,  4,  5,  1,  3,  3, 10,  3]
])
collision_ypos = np.array([
    [1,  3,  5,  7,  4,  5,  1,  8,  5,  4,  4,  8,  7,  6,  3,  9,
     2,  8,  3,  7,  6, 10,  6,  1,  8],
    [4,  1,  8,  5,  2,  7,  1,  7,  4,  6,  6,  9,  5,  6,  9,  6,
     1,  2,  6,  1,  0, 10,  2,  2,  6]
])

no_collision_xpos = np.array([
    [8,  9,  1,  4,  6,  3,  6,  6,  1,  4,  2,  7,  7,  4,  2,  0,
     7,  4,  5,  1,  5,  2,  3,  8,  5],
    [6,  9,  7,  9,  4,  2,  3,  6,  6,  5,  5,  0,  5,  4,  2,  9,
     5,  7,  4,  6,  6,  7,  3,  9,  9]
])
no_collision_ypos = np.array([
    [3,  8,  3,  8,  4,  8,  3,  0,  1,  1,  7,  5,  5,  4,  4, 10,
     9,  0,  7,  9,  9,  3,  1,  5,  1],
    [8,  7,  3,  8,  9,  2,  8,  6,  9,  6, 10,  9,  3,  1,  2,  7,
     9,  1, 10,  2,  1,  0,  2,  6,  8]
])

class TestDemo(unittest.TestCase):
    def run_simple(self, **kwargs):
        params.steps = 'all'
        params.one_time_pad_length = 64
        params.num_users = 2
        params.num_user_log_per_hour = 1
        params.num_patient_zeros = 1
        params.basedir = 'demo'
        params.num_days = 1
        params.xmax = 10
        params.debug = False
        for k in kwargs.keys():
            params.__dict__[k] = kwargs[k]
        return drive(params)

    @patch(
        "demo.runenv.brownian",
        side_effect=[collision_xpos, collision_ypos]
    )
    def test_one_collision(self, mock):
        runlog = self.run_simple()[0]
        self.assertEqual(runlog['users_notified'], [0, 1])
        expected_contacts = defaultdict(list)
        expected_contacts[6] = [(0, 1, (7, 1))]
        contacts = runlog['new_contacts']
        self.assertEqual(contacts.keys(), expected_contacts.keys())
        self.assertEqual(contacts[6], expected_contacts[6])
        self.assertEqual(runlog['new_diagnosed_patients'], [0])
        self.assertEqual(runlog['num_results_responsible'],  25)
        self.assertEqual(runlog['num_publishes_for_other_location_auths'], 0)
        self.assertEqual(runlog['num_notifications'], 26)

    @patch(
        "demo.runenv.brownian",
        side_effect=[no_collision_xpos, no_collision_ypos]
    )
    def test_no_collision(self, mock):
        runlog = self.run_simple()[0]
        self.assertEqual(runlog['users_notified'], [0])
        self.assertEqual(runlog['new_diagnosed_patients'], [0])
        self.assertEqual(runlog['num_results_responsible'],  25)
        self.assertEqual(runlog['num_publishes_for_other_location_auths'], 0)
        self.assertEqual(runlog['num_notifications'], 25)
        new_contacts = runlog['new_contacts']
        self.assertEqual(len(new_contacts), 0)

    def test_random_runs(self):
        test_counter = defaultdict(int)
        for i in range(3):
            runlog = self.run_simple(xmax=3, num_days=5)[0]
            num_users_notified = len(runlog['users_notified'])
            self.assertTrue(num_users_notified == 1 or num_users_notified == 2)
            if num_users_notified == 1:
                self.assertEqual(runlog['users_notified'], [0])
                u0_pos = zip(runlog['xpos'][0], runlog['ypos'][0])
                u1_pos = zip(runlog['xpos'][1], runlog['ypos'][1])
                for u0, u1 in zip(u0_pos, u1_pos):
                    self.assertNotEqual(u0, u1)
                test_counter[1] += 1
            if num_users_notified == 2:
                self.assertEqual(runlog['users_notified'], [0, 1])
                u0_pos = zip(runlog['xpos'][0], runlog['ypos'][0])
                u1_pos = zip(runlog['xpos'][1], runlog['ypos'][1])
                both_pos = list(zip(u0_pos, u1_pos))
                for k, v in runlog['new_contacts'].items():
                    positions = both_pos[k]
                    self.assertEqual(positions[0], positions[1])
                for i, b in enumerate(both_pos):
                    if i not in runlog['new_contacts'].keys():
                        self.assertNotEqual(b[0], b[1])
                test_counter[2] += 1

        self.assertGreater(test_counter[1], 0)
        # below fails with 1.21e-6 chance: (1-1/3**2)**(25*5)*3
        self.assertGreater(test_counter[2], 0)

if __name__ == '__main__':
    unittest.main()
