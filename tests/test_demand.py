from unittest import TestCase

from entities.demand import Demand


class TestDemand(TestCase):

    def test_checking_correct_operation_of_counter_id(self):
        demand0 = Demand(arrival_time=0, class_id=0, fragments_amount=2)
        self.assertEqual(demand0.id, 0)

        demand1 = Demand(arrival_time=0, class_id=0, fragments_amount=2)
        self.assertEqual(demand1.id, 1)
