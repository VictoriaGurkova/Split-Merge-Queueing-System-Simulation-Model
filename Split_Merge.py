from Demand import Demand
from queue import Queue
from random import expovariate, choice

from Wrapper_for_Devices import Wrapper_for_Devices


class SplitMerge:
    def __init__(self, la, mu, amount_of_devices, list_of_amounts_fragments):
        self.Lambda = la
        self.current_time = 0
        self.arrival_time = expovariate(la)
        self.service_start_time = float('inf')
        self.leaving_time = float('inf')
        # для статистики
        self.amount_of_served_demands = 0
        self.average_time_demands_in_network = 0

        # список, состоящий из элементов, обозн. количество фрагментов в каждом классе требований
        self.list_of_amounts_fragments = list_of_amounts_fragments
        self.wrapper = Wrapper_for_Devices(mu, amount_of_devices)
        # генерируются очереди, количество которых равно количеству классов требований
        self.list_of_queues = [Queue() for _ in range(len(list_of_amounts_fragments))]

    # обрабатывает поступление требований в сеть
    def arrival_of_demand(self):
        # рандомно создается требование 1го или 2го класса TODO: добавить в Demand конкретный класс
        demand = Demand(self.arrival_time, choice(self.list_of_amounts_fragments))
        # индекс очереди для определённого класса требований
        # TODO: сделать очередь списком
        index_of_class = self.list_of_amounts_fragments.index(demand.amount_of_fragments)
        # если очередь данного класса пуста и свободных приборов больше либо равно чем фрагментов требования
        # TODO: вынести вфункцию can_occupy
        if self.list_of_queues[index_of_class].empty() and \
                self.wrapper.get_amount_of_free_devices() >= demand.amount_of_fragments:
            # устанавливаем время начала обслуживания
            self.service_start_time = self.current_time
        # требование помещается в очередь соответствующего класса
        self.list_of_queues[index_of_class].put(demand)
        # планируется время поступления следующего требования
        self.arrival_time += expovariate(self.Lambda)

    def demand_service_start(self):
        # TODO: вынести в функцию if_possible
        # TODO: сделать for, чтобы можно было проверять любое количество очередей
        if self.wrapper.get_amount_of_free_devices() >= self.list_of_amounts_fragments[0]:
            demand = self.list_of_queues[0].get()
            self.wrapper.distribute_fragments(demand)
        else:
            demand = self.list_of_queues[1].get()
            self.wrapper.distribute_fragments(demand)
        demand.service_start_time = self.current_time
        self.leaving_time = self.current_time + self.wrapper.get_min_service_duration_for_demand()
        # !!!
        self.service_start_time = float('inf')


if __name__ == '__main__':
    pass
