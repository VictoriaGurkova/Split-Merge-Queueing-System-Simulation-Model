from Demand import Demand
from Device import Device
from queue import Queue
from random import expovariate, choice

from Wrapper_for_Devices import Wrapper_for_Devices


class SplitMerge:
    def __init__(self, la, mu, amount_of_devices, list_of_amounts_fragments):
        self.la = la
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
        self.list_of_queues = [Queue() for _ in range(len(list_of_amounts_fragments))]

    # обрабатывает поступление требований в сеть
    def arrival_of_demand(self):
        # рандомно создается требование 1го или 2го класса
        demand = Demand(self.arrival_time, choice(self.list_of_amounts_fragments))
        # индекс очереди для определённого класса требований
        index_of_class = self.list_of_amounts_fragments.index(demand.amount_of_fragments)
        # если очередь данного класса пуста и свободных приборов больше либо равно чем фрагментов требования
        if self.list_of_queues[index_of_class].empty() and \
                self.wrapper.get_amount_of_free_devices() >= demand.amount_of_fragments:
            # устанавливаем время начала обслуживания
            self.service_start_time = self.current_time
        # требование помещается в очередь соответствующего класса
        self.list_of_queues[index_of_class].put(demand)
        # планируется время поступления следующего требования
        self.arrival_time += expovariate(self.la)

    def start_service_demand(self):
        pass


if __name__ == '__main__':
    pass
