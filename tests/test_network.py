from unittest import TestCase
from unittest import skip

from src.network_simulation import SplitMergeSystem


class TestSplitMergeSystem(TestCase):

    @skip
    def test_run(self):
        self.fail()

    @skip
    def test__arrival_of_demand(self):
        self.fail()

    @skip
    def test__demand_service_start(self):
        self.fail()

    @skip
    def test__leaving_demand(self):
        self.fail()

    @skip
    def test__set_events_times(self):
        self.fail()

    def test__define_arriving_demand_class(self):
        self.assertEqual(SplitMergeSystem._define_arriving_demand_class(probability=1), 0)
        self.assertEqual(SplitMergeSystem._define_arriving_demand_class(probability=0), 1)
