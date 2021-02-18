from unittest import TestCase

from entities.fragment import Fragment


class TestFragment(TestCase):

    def test_checking_correct_operation_of_counter_id(self):
        Fragment._reset_counter()
        fragment0 = Fragment(parent_id=0)
        self.assertEqual(fragment0.id, 0)

        fragment1 = Fragment(parent_id=1)
        self.assertEqual(fragment1.id, 1)
