from unittest import TestCase

from clock import Clock


class TestClock(TestCase):

    def test_update_arrival_time(self):
        times = Clock()
        self.assertEqual(times.arrival, 0)
        times.update_arrival_time(rate=1)
        self.assertNotEqual(times.arrival, 0)
