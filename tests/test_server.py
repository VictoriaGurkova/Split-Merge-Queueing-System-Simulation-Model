from unittest import TestCase

from src.entities.server import Server
from src.entities.fragment import Fragment


class TestServer(TestCase):

    def setUp(self) -> None:
        rate = 1
        self.server = Server(rate)
        self.fragment = Fragment(parent_id=1)

    def test_to_occupy(self) -> None:
        self._check_server_state_free()
        self.server.to_occupy(self.fragment, current_time=1)
        self._check_server_state_not_free()

    def test_to_free(self) -> None:
        self.server.to_occupy(self.fragment, current_time=1)
        self._check_server_state_not_free()
        self.server.to_free()
        self._check_server_state_free()

    def _check_server_state_free(self) -> None:
        self.assertTrue(self.server.is_free)
        self.assertIsNone(self.server.fragment)

    def _check_server_state_not_free(self) -> None:
        self.assertFalse(self.server.is_free)
        self.assertEqual(self.server.fragment, self.fragment)
