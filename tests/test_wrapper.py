from random import randint
from unittest import TestCase, skip

from entities.demand import Demand
from entities.wrapper import DevicesWrapper


class TestDevicesWrapper(TestCase):

    def setUp(self) -> None:
        self.amount_of_devices = randint(2, 10)
        self.wrapper = DevicesWrapper(mu=1, amount_of_devices=self.amount_of_devices)

    @skip
    def test_distribute_fragments(self):
        self.fail()

    def test_get_amount_of_free_devices(self):
        self.assertEqual(self.wrapper.get_amount_of_free_devices(), self.amount_of_devices)

        fragments_amount = randint(1, self.amount_of_devices)
        self.wrapper.distribute_fragments(Demand(arrival_time=0,
                                                 class_id=0,
                                                 fragments_amount=fragments_amount),
                                          current_time=0)
        self.assertEqual(self.wrapper.get_amount_of_free_devices(), self.amount_of_devices - fragments_amount)

    # TODO: дописать
    @skip
    def test_get_min_end_service_time_for_demand(self):
        self.wrapper.distribute_fragments(Demand(arrival_time=0,
                                                 class_id=0,
                                                 fragments_amount=randint(1, self.amount_of_devices)),
                                          current_time=0)

    @skip
    def test_get_service_duration_fragments(self):
        self.fail()

    @skip
    def test_get_id_demands_on_devices(self):
        self.fail()

    @skip
    def test_get_demand_id_with_min_end_service_time(self):
        self.fail()

    @skip
    def test_to_free_demand_fragments(self):
        self.fail()

    @skip
    def test_can_occupy(self):
        self.fail()

    @skip
    def test_check_if_possible_put_demand_on_devices(self):
        self.fail()
