from unittest import TestCase

from entities.device import Device
from entities.fragment import Fragment


class TestDevice(TestCase):

    def setUp(self) -> None:
        rate = 1
        self.device = Device(rate)
        self.fragment = Fragment(parent_id=1)

    def test_to_occupy(self) -> None:
        self._check_device_state_free()
        self.device.to_occupy(self.fragment, current_time=1)
        self._check_device_state_not_free()

    def test_to_free(self) -> None:
        self.device.to_occupy(self.fragment, current_time=1)
        self._check_device_state_not_free()
        self.device.to_free()
        self._check_device_state_free()

    def _check_device_state_free(self) -> None:
        self.assertTrue(self.device.is_free)
        self.assertIsNone(self.device.fragment)

    def _check_device_state_not_free(self) -> None:
        self.assertFalse(self.device.is_free)
        self.assertEqual(self.device.fragment, self.fragment)
