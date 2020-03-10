import time
from random import expovariate, randint
import logging

from Demand import Demand
from Wrapper_for_Devices import Wrapper_for_Devices


class SplitMerge:
    def __init__(self, la, mu, amount_of_devices, list_of_amounts_fragments):
        self.Lambda = la
        self.current_time = 0
        self.arrival_time = expovariate(la)
        self.service_start_time = float('inf')
        self.leaving_time = float('inf')
        self.amount_of_served_demands = 0
        self.time_demands_in_network = 0

        self.list_of_demands_in_network = []
        # список, состоящий из элементов, обозн. количество фрагментов в каждом классе требований
        self.list_of_amounts_fragments = list_of_amounts_fragments
        self.wrapper = Wrapper_for_Devices(mu, amount_of_devices)
        # генерируются очереди, количество которых равно количеству классов требований
        self.list_of_queues = [[] for _ in range(len(list_of_amounts_fragments))]
        logging.basicConfig(filename="split_merge.log", level=logging.DEBUG, filemode="w")

    # обрабатывает поступление требований в сеть
    def arrival_of_demand(self):
        demand_class_id = randint(0, len(self.list_of_amounts_fragments) - 1)
        demand = Demand(self.arrival_time, demand_class_id, self.list_of_amounts_fragments[demand_class_id])
        logging.debug("Demand arrival: ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                      " . Current Time: " + str(self.current_time))
        if self.can_occupy_devices(demand.class_id):
            self.service_start_time = self.current_time
        self.list_of_queues[demand_class_id].append(demand)
        # планируется время поступления следующего требования
        self.arrival_time += expovariate(self.Lambda)

    def demand_service_start(self):
        try:
            demand = None
            for class_id in range(len(self.list_of_amounts_fragments)):
                if self.can_occupy_devices(class_id):
                    demand = self.list_of_queues[class_id].pop(0)
                    logging.debug("Demand start service: ID - " + str(demand.id) + " . Class ID - " +
                                  str(demand.class_id) + " . Current Time: " + str(self.current_time))
                    self.wrapper.distribute_fragments(demand)
                    self.list_of_demands_in_network.append(demand)
                    break
            demand.service_start_time = self.current_time
        finally:
            self.leaving_time = self.current_time + self.wrapper.get_min_service_duration_for_demand()
            self.service_start_time = float('inf')

    def leaving_demand(self):
        leaving_demand_id = self.wrapper.get_id_demand_with_min_service_duration()
        self.wrapper.to_free_demand_fragments(leaving_demand_id)
        demand = None
        for d in self.list_of_demands_in_network:
            if d.id == leaving_demand_id:
                demand = d
                break
        logging.debug("Demand leaving: ID - " + str(demand.id) + " . Class ID - " + str(demand.class_id) +
                      " . Current Time: " + str(self.current_time))
        demand.leaving_time = self.current_time
        self.time_demands_in_network += demand.leaving_time - demand.arrival_time
        if self.check_if_possible_put_demand_on_devices():
            self.service_start_time = self.current_time
        self.leaving_time = float('inf')

    def main(self, max_time):
        while self.current_time < max_time:
            self.current_time = min(self.arrival_time, self.service_start_time, self.leaving_time)
            if self.current_time == self.arrival_time:
                self.arrival_of_demand()
                time.sleep(0.2)
                continue
            if self.current_time == self.service_start_time:
                self.demand_service_start()
                time.sleep(0.2)
                continue
            if self.current_time == self.leaving_time:
                self.leaving_demand()
                time.sleep(0.2)
                continue
        print(self.time_demands_in_network / self.amount_of_served_demands)

    def can_occupy_devices(self, class_id):
        return self.list_of_queues[class_id] and \
               self.wrapper.get_amount_of_free_devices() >= self.list_of_amounts_fragments[class_id]

    def check_if_possible_put_demand_on_devices(self):
        return len(
            [True for class_id in range(len(self.list_of_amounts_fragments)) if self.can_occupy_devices(class_id)])


if __name__ == '__main__':
    sp = SplitMerge(0.5, 1, 3, [1, 2])
    sp.main(100)
