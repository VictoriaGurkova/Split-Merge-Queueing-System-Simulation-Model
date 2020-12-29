import logging
from random import expovariate, random

from ProgressBar import ProgressBar
from Statistics import Statistics
from entities.WrapperForDevices import WrapperForDevices
from entities.Demand import Demand


class SplitMerge:
    """Class describing the simulation model split-merge simulation model of a queuing system

    Two classes of demand, two queues for demand.
    The progression of simulation time is from event to event.
    Events: arrival demand, start service demand and leaving demand

    """

    def __init__(self, lambda1: float, lambda2: float,
                 mu: float,
                 amount_of_devices: int,
                 amounts_of_fragments: list,
                 dimension_of_queues: list,
                 statistics: Statistics):
        """

        :param lambda1: intensity of the incoming flow of first class demand
        :param lambda2: intensity of the incoming flow of second class demand
        :param mu: service rate of a demand by one device
        :param amount_of_devices: number of devices in the system
        :param amounts_of_fragments: view [a, b], where a is the number of fragments of the first class demand
        and b - second demand
        :param dimension_of_queues: queue dimensions, similarly as list_amounts_of_fragments
        :param statistics: variable for counting and calculating statistics
        """
        self._lambda1 = lambda1
        self._lambda2 = lambda2
        self._lambda = lambda1 + lambda2
        self._prob1 = lambda1 / self._lambda

        self._dimension_of_queues = dimension_of_queues

        self._current_time = 0
        self._arrival_time = expovariate(self._lambda)
        self._service_start_time = float('inf')
        self._leaving_time = float('inf')

        self._statistics = statistics

        self._demands_in_network = []
        self._served_demands = []
        self._amounts_of_fragments = amounts_of_fragments
        self._wrapper = WrapperForDevices(mu, amount_of_devices)
        self._queues = list([] for _ in range(len(amounts_of_fragments)))

        logging.basicConfig(filename="logging.log", level=logging.ERROR, filemode="w")

    def arrival_of_demand(self):
        """Event describing the arrival of a demand to the system"""

        class_id = self.get_id_arrived_demand()
        demand = Demand(self._arrival_time, class_id, self._amounts_of_fragments[class_id])

        if len(self._queues[class_id]) < self._dimension_of_queues[class_id]:
            self._service_start_time = self._current_time
            self._queues[class_id].append(demand)

            logging.debug("Demand arrival: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                          ". Current Time: " + str(self._current_time))
        else:
            logging.debug(
                "Demand arrival (FULL QUEUE): ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                ". Current Time: " + str(self._current_time))
        # set arrival time of the next demand
        self._arrival_time += expovariate(self._lambda)

    def get_id_arrived_demand(self):
        """Definition of the demand class"""
        return 0 if random() < self._prob1 else 1

    def demand_service_start(self):
        """Event describing the start of servicing a demand"""

        # take demand from all queues in direct order
        for class_id in range(len(self._amounts_of_fragments)):
            while self.can_occupy(class_id) and self._queues[class_id]:
                demand = self._queues[class_id].pop(0)
                # scattering fragments across systems
                self._wrapper.distribute_fragments(demand, self._current_time)
                self._demands_in_network.append(demand)
                demand.service_start_time = self._current_time

                logging.debug("Demand start service: ID - " + str(demand.id) + ". Class ID - " +
                              str(demand.class_id) + ". Current Time: " + str(self._current_time))

        self._service_start_time = float('inf')

        # take the near term of the end of servicing demands
        if self._wrapper.get_id_demands_on_devices():
            self._leaving_time = self._wrapper.get_min_end_service_time_for_demand()

    def leaving_demand(self):
        """Event describing a demand leaving the system"""

        leaving_demand_id = self._wrapper.get_demand_id_with_min_end_service_time()
        self._wrapper.to_free_demand_fragments(leaving_demand_id)
        demand = None

        # free all devices with fragments of the given id
        for d in self._demands_in_network:
            if d.id == leaving_demand_id:
                demand = d
                self._demands_in_network.remove(demand)
                break

        demand.leaving_time = self._current_time
        self._served_demands.append(demand)
        self.set_times()

        logging.debug("Demand leaving: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                      ". Current Time: " + str(self._current_time))

    def set_times(self):
        if self.check_if_possible_put_demand_on_devices():
            self._service_start_time = self._current_time
        if not self._wrapper.get_id_demands_on_devices():
            self._leaving_time = float('inf')
        else:
            self._leaving_time = self._wrapper.get_min_end_service_time_for_demand()

    def main(self, simulation_time: int):
        """

        :param simulation_time: model simulation duration
        """
        bar = ProgressBar(0, 'Progress: ')

        # process of simulating a split-merge system
        while self._current_time <= simulation_time:
            # take the time of the nearest events
            self._current_time = min(self._arrival_time, self._service_start_time, self._leaving_time)

            bar.print_progress(self._current_time, simulation_time)

            logging.debug("Device's state: " + str(self._wrapper.get_id_demands_on_devices()))
            logging.debug("Device's state with min time: " + str(self._wrapper.get_service_duration_fragments()))
            logging.debug("Event times: = " + str([self._arrival_time, self._service_start_time, self._leaving_time]))

            if self._current_time == self._arrival_time:
                self.arrival_of_demand()
                continue
            if self._current_time == self._service_start_time:
                self.demand_service_start()
                continue
            if self._current_time == self._leaving_time:
                self.leaving_demand()
                continue

        print()
        self._statistics.record(self._served_demands)

    def can_occupy(self, class_id: int):
        """Checking whether the demand of this class can take place on the devices

        :param class_id: demand class
        """
        return self._wrapper.get_amount_of_free_devices() >= self._amounts_of_fragments[class_id]

    def check_if_possible_put_demand_on_devices(self):
        """Checking whether it is possible to place a demand on devices"""

        return len([True for class_id in range(len(self._amounts_of_fragments))
                    if self.can_occupy(class_id)])
