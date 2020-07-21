import logging
from random import expovariate, random

from Demand import Demand
from ProgressBar import ProgressBar
from Statistics import Statistics
from WrapperForDevices import WrapperForDevices


class SplitMerge:
    def __init__(self, la1: float, la2: float,
                 mu: float,
                 amount_of_devices: int,
                 list_amounts_of_fragments: list,
                 capacity: list,
                 statistics: Statistics):
        # два пуассоновских потока дадут суммарно пуассоновский поток
        # интенсивности при это суммируются
        # а требование будет иметь первый класс с веростностью la1/(la1 + la2) - эту вероятность _prob1 будем
        # использовать далее в соответ методе

        self._la1 = la1
        self._la2 = la2
        self._la = la1 + la2
        self._prob1 = la1 / self._la

        self._capacity = capacity

        self._current_time = 0
        self._arrival_time = expovariate(self._la)
        self._service_start_time = float('inf')
        self._leaving_time = float('inf')

        self._statistics = statistics

        self._list_of_demands_in_network = []
        self._list_of_served_demands = []
        self._list_amounts_of_fragments = list_amounts_of_fragments
        self._wrapper = WrapperForDevices(mu, amount_of_devices)
        self._list_of_queues = list([] for _ in range(len(list_amounts_of_fragments)))

        logging.basicConfig(filename="split_merge.log", level=logging.ERROR, filemode="w")

    def arrival_of_demand(self):
        # если рандомное число оказалось меньше (первая часть отрезка), то это равносильно тому,
        # что поступающее требование было первого класса
        if random() < self._prob1:
            demand_class_id = 0
        else:
            demand_class_id = 1

        demand = Demand(self._arrival_time, demand_class_id, self._list_amounts_of_fragments[demand_class_id])
        if len(self._list_of_queues[demand_class_id]) < self._capacity[demand_class_id]:
            self._service_start_time = self._current_time
            self._list_of_queues[demand_class_id].append(demand)
            logging.debug("Demand arrival: ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                          " . Current Time: " + str(self._current_time))
        else:
            logging.debug(
                "Demand arrival (FULL QUEUE): ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                " . Current Time: " + str(self._current_time))
        self._arrival_time += expovariate(self._la)

    def demand_service_start(self):
        # начинаем забирать требования со всех очередей по порядку 1, 2, ...
        for class_id in range(len(self._list_amounts_of_fragments)):
            while self.can_occupy(class_id) and self._list_of_queues[class_id]:
                demand = self._list_of_queues[class_id].pop(0)
                self._wrapper.distribute_fragments(demand, self._current_time)
                self._list_of_demands_in_network.append(demand)
                demand.service_start_time = self._current_time
                logging.debug("Demand start service: ID - " + str(demand.id) + " . Class ID - " +
                              str(demand.class_id) + " . Current Time: " + str(self._current_time))

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
                self._list_of_demands_in_network.remove(demand)
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

    def main(self, simulation_time: int):
        bar = ProgressBar(0, 'Progress: ')

        while self._current_time < simulation_time:
            self._current_time = min(self._arrival_time, self._service_start_time, self._leaving_time)

            bar.print_progress(self._current_time, simulation_time)

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
        print()
        self._statistics.record(self._list_of_served_demands)

    def can_occupy(self, class_id: int):
        return self._wrapper.get_amount_of_free_devices() >= \
               self._list_amounts_of_fragments[class_id]

    def check_if_possible_put_demand_on_devices(self):
        return len([True for class_id in range(len(self._list_amounts_of_fragments))
                    if self.can_occupy(class_id)])
