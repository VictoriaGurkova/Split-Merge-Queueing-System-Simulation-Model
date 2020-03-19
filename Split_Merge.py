import time
from random import expovariate, randint
import logging

from Demand import Demand
from Statistics import Statistics
from Wrapper_for_Devices import Wrapper_for_Devices


class SplitMerge:
    def __init__(self, la: float, mu: float, amount_of_devices: int, list_amounts_of_fragments: list,
                 statistics: Statistics):
        self._la = la
        self._current_time = 0
        self._arrival_time = expovariate(la)
        self._service_start_time = float('inf')
        self._leaving_time = float('inf')
        self._statistics = statistics

        self._list_of_demands_in_network = []
        self._list_of_served_demands = []
        self._list_amounts_of_fragments = list_amounts_of_fragments
        self._wrapper = Wrapper_for_Devices(mu, amount_of_devices)
        self._list_of_queues = list([] for _ in range(len(list_amounts_of_fragments)))

        logging.basicConfig(filename="split_merge.log", level=logging.DEBUG, filemode="w")

    def arrival_of_demand(self):
        demand_class_id = randint(0, len(self._list_amounts_of_fragments) - 1)
        demand = Demand(self._arrival_time, demand_class_id, self._list_amounts_of_fragments[demand_class_id])
        self._service_start_time = self._current_time
        self._list_of_queues[demand_class_id].append(demand)
        self._arrival_time += expovariate(self._la)

        logging.debug("Demand arrival: ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                      " . Current Time: " + str(self._current_time))

    def demand_service_start(self):
        for class_id in range(len(self._list_amounts_of_fragments)):
            while True:
                if self.can_occupy(class_id) and self._list_of_queues[class_id]:
                    demand = self._list_of_queues[class_id].pop(0)
                    self._wrapper.distribute_fragments(demand, self._current_time)
                    self._list_of_demands_in_network.append(demand)
                    demand.service_start_time = self._current_time

                    logging.debug("Demand start service: ID - " + str(demand.id) + " . Class ID - " +
                                  str(demand.class_id) + " . Current Time: " + str(self._current_time))
                else:
                    break
        self._service_start_time = float('inf')
        if self._wrapper.get_id_demands_on_devices():
            self._leaving_time = self._wrapper.get_min_end_service_time_for_demand()

    def leaving_demand(self):
        leaving_demand_id = self._wrapper.get_id_demand_with_min_end_service_time()
        self._wrapper.to_free_demand_fragments(leaving_demand_id)
        demand = None
        for d in self._list_of_demands_in_network:
            if d.id == leaving_demand_id:
                demand = d
                break
        demand.leaving_time = self._current_time
        self._list_of_served_demands.append(demand)
        if self.check_if_possible_put_demand_on_devices():
            self._service_start_time = self._current_time
        if not self._wrapper.get_id_demands_on_devices():
            self._leaving_time = float('inf')
        else:
            self._leaving_time = self._wrapper.get_min_end_service_time_for_demand()

        logging.debug("Demand leaving: ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                      " . Current Time: " + str(self._current_time))

    def main(self, max_time):
        while self._current_time < max_time:
            self._current_time = min(self._arrival_time, self._service_start_time, self._leaving_time)
            logging.debug("Device's state: " + str(self._wrapper.get_id_demands_on_devices()))
            logging.debug(
                "Device's state with min time: " + str(self._wrapper.get_lists_of_service_duration_fragments()))
            logging.debug("event times: = " + str([self._arrival_time, self._service_start_time, self._leaving_time]))
            if self._current_time == self._arrival_time:
                self.arrival_of_demand()
                continue
            if self._current_time == self._service_start_time:
                self.demand_service_start()
                continue
            if self._current_time == self._leaving_time:
                self.leaving_demand()
                continue
        self._statistics.record(self._list_of_served_demands)

    def can_occupy(self, class_id):
        return self._wrapper.get_amount_of_free_devices() >= self._list_amounts_of_fragments[class_id]

    def check_if_possible_put_demand_on_devices(self):
        return len([True for class_id in range(len(self._list_amounts_of_fragments)) if self.can_occupy(class_id)])
