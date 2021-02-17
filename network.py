from random import random

from clock import Clock
from entities.demand import Demand
from entities.wrapper import DevicesWrapper
from logs import log_arrival, log_full_queue, log_service_start, log_leaving, log_network_state
from network_params import Params
from progress_bar import ProgressBar
from statistics import Statistics


class SplitMergeSystem:
    """Class describing the simulation model split-merge simulation model of a queuing system

    Two classes of demand, two queues for demand.
    The progression of simulation time is from event to event.
    Events: arrival demand, start service demand and leaving demand

    """

    def __init__(self,
                 params: Params,
                 progress_bar: ProgressBar):
        """

        @param params:
        @param progress_bar:
        """

        self.params = params
        self.progress_bar = progress_bar

        self.times = Clock()
        # устанавливаем время прибытия требования
        self.times.update_arrival_time(params.combined_lambda)
        self.statistics = Statistics(params.fragments_amounts)

        self.first_class_arrival_probability = params.lambda1 / params.combined_lambda

        # TODO: создать дата-класс для конфигурации сети
        # network configuration - number of queues and devices
        self.config = {
            "queues": list([] for _ in range(len(params.fragments_amounts))),  # view: [[], []]
        }
        self.devices = DevicesWrapper(params.mu, params.devices_amount)

        self.demands_in_network = []
        self.served_demands = []

    def arrival_of_demand(self):
        """Event describing the arrival of a demand to the system"""

        class_id = define_arriving_demand_class(self.first_class_arrival_probability)
        demand = Demand(self.times.arrival,
                        class_id, self.params.fragments_amounts[class_id])

        if len(self.config["queues"][class_id]) < self.params.queues_capacities[class_id]:
            self.times.service_start = self.times.current
            self.config["queues"][class_id].append(demand)
            log_arrival(demand, self.times.current)
        else:
            log_full_queue(demand, self.times.current)

        self.times.update_arrival_time(self.params.combined_lambda)

    def demand_service_start(self):
        """Event describing the start of servicing a demand"""

        # take demand from all queues in direct order
        for class_id in range(len(self.params.fragments_amounts)):
            while self.devices.can_occupy(class_id, self.params) and self.config["queues"][class_id]:
                demand = self.config["queues"][class_id].pop(0)
                self.devices.distribute_fragments(demand, self.times.current)
                self.demands_in_network.append(demand)
                demand.service_start_time = self.times.current
                log_service_start(demand, self.times.current)

        self.times.service_start = float('inf')

        # take the near term of the end of servicing demands
        if self.devices.get_id_demands_on_devices():
            self.times.leaving = self.devices.get_min_end_service_time_for_demand()

    def leaving_demand(self):
        """Event describing a demand leaving the system"""

        leaving_demand_id = self.devices.get_demand_id_with_min_end_service_time()
        self.devices.to_free_demand_fragments(leaving_demand_id)
        demand = None

        for d in self.demands_in_network:
            if d.id == leaving_demand_id:
                demand = d
                self.demands_in_network.remove(demand)
                break

        demand.leaving_time = self.times.current
        self.served_demands.append(demand)
        set_events_times(self.times, self.devices, self.params)

        log_leaving(demand, self.times.current)

    def run(self, simulation_time: int) -> Statistics:
        """

        @param simulation_time: model simulation duration
        """

        while self.times.current <= simulation_time:
            self.times.current = min(self.times.arrival, self.times.service_start, self.times.leaving)

            self.progress_bar.update_progress(self.times.current, simulation_time)
            log_network_state(self.times, self.devices)

            if self.times.current == self.times.arrival:
                self.arrival_of_demand()
                continue
            if self.times.current == self.times.service_start:
                self.demand_service_start()
                continue
            if self.times.current == self.times.leaving:
                self.leaving_demand()
                continue

        self.statistics.calculate_stat(self.served_demands)
        return self.statistics


def define_arriving_demand_class(probability: float):
    return 0 if random() < probability else 1


def set_events_times(times: Clock, devices: DevicesWrapper, params: Params):
    if devices.check_if_possible_put_demand_on_devices(params):
        times.service_start = times.current
    if not devices.get_id_demands_on_devices():
        times.leaving = float('inf')
    else:
        times.leaving = devices.get_min_end_service_time_for_demand()
