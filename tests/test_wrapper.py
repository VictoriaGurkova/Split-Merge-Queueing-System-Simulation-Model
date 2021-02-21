from random import randint
from unittest import TestCase, skip

from entities.demand import Demand
from entities.wrapper import ServersWrapper


class TestServersWrapper(TestCase):

    def setUp(self) -> None:
        self.servers_number = randint(2, 10)
        self.wrapper = ServersWrapper(mu=1, servers_number=self.servers_number)

    @skip
    def test_distribute_fragments(self):
        self.fail()

    def test_get_number_of_free_servers(self):
        self.assertEqual(self.wrapper.get_number_of_free_servers(), self.servers_number)

        fragments_number = randint(1, self.servers_number)
        self.wrapper.distribute_fragments(Demand(arrival_time=0,
                                                 class_id=0,
                                                 fragments_number=fragments_number),
                                          current_time=0)
        self.assertEqual(self.wrapper.get_number_of_free_servers(), self.servers_number - fragments_number)

    # TODO: дописать
    @skip
    def test_get_min_end_service_time_for_demand(self):
        self.wrapper.distribute_fragments(Demand(arrival_time=0,
                                                 class_id=0,
                                                 fragments_number=randint(1, self.servers_number)),
                                          current_time=0)

    @skip
    def test_get_fragments_service_duration(self):
        self.fail()

    @skip
    def test_get_demands_ids_on_servers(self):
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
    def test_check_if_possible_put_demand_on_servers(self):
        self.fail()
