from unittest import TestCase

from clock import Clock


class TestClock(TestCase):

    def test_update_arrival_time(self):
        times = Clock()
        default_arrival_value = 0

        self.assertEqual(times.arrival, default_arrival_value)
        times.update_arrival_time(rate=1)
        self.assertNotEqual(times.arrival, default_arrival_value)
