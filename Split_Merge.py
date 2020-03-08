from random import expovariate, randint

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
        self.average_time_demands_in_network = 0

        # список, состоящий из элементов, обозн. количество фрагментов в каждом классе требований
        self.list_of_amounts_fragments = list_of_amounts_fragments
        self.wrapper = Wrapper_for_Devices(mu, amount_of_devices)
        # генерируются очереди, количество которых равно количеству классов требований
        self.list_of_queues = [[] for _ in range(len(list_of_amounts_fragments))]

    # обрабатывает поступление требований в сеть
    def arrival_of_demand(self):
        demand_class_id = randint(0, len(self.list_of_amounts_fragments) - 1)
        demand = Demand(self.arrival_time, demand_class_id, self.list_of_amounts_fragments[demand_class_id])
        if self.can_occupy(demand):
            self.service_start_time = self.current_time
        self.list_of_queues[demand_class_id].append(demand)
        # планируется время поступления следующего требования
        self.arrival_time += expovariate(self.Lambda)

    def demand_service_start(self):
        try:
            demand = None
            for i in range(len(self.list_of_amounts_fragments)):
                if self.can_take_demand_for_service(i):
                    demand = self.list_of_queues[i].pop(0)
                    self.wrapper.distribute_fragments(demand)
                    break
            demand.service_start_time = self.current_time
        finally:
            self.leaving_time = self.current_time + self.wrapper.get_min_service_duration_for_demand()
            self.service_start_time = float('inf')

    # проверяется, может ли требрвания поместиться на приборы
    def can_occupy(self, demand):
        return not self.list_of_queues[demand.class_id] and \
            self.wrapper.get_amount_of_free_devices() >= demand.amount_of_fragments

    def can_take_demand_for_service(self, i):
        return self.wrapper.get_amount_of_free_devices() >= self.list_of_amounts_fragments[i]


if __name__ == '__main__':
    pass
