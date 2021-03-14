from random import random

from clock import Clock
from entities.demand import Demand
from entities.wrapper import ServersWrapper
from logs import log_arrival, log_full_queue, log_service_start, log_leaving, log_network_state
from network_params import Params
from progress_bar import ProgressBar
from statistics import Statistics


class SplitMergeSystem:
    """This class describes the split-merge queuing system simulation model.

    Two classes of demand, two queues for demand.
    The progression of simulation time is from event to event.
    Events: arrival demand, start service demand and leaving demand

    """

    def __init__(self,
                 params: Params,
                 progress_bar: ProgressBar,
                 selection_policy):
        """

        @param params:
        @param progress_bar:
        @param selection_policy:
        """

        self._selection_policy = selection_policy
        self._params = params
        self._progress_bar = progress_bar

        self._times = Clock()
        # устанавливаем время прибытия первого требования
        self._times.update_arrival_time(params.combined_lambda)

        self._first_class_arrival_probability = params.lambda1 / params.combined_lambda

        self._queues = [[] for _ in range(len(params.fragments_numbers))]
        self._servers = ServersWrapper(params.mu, params.servers_number)

        self._demands_in_network = []
        self._served_demands = []

    def run(self, simulation_time: int) -> Statistics:
        """

        @param simulation_time: model simulation duration
        """

        statistics = Statistics(self._params.fragments_numbers)

        while self._times.current <= simulation_time:
            self._times.current = min(self._times.arrival, self._times.service_start, self._times.leaving)

            self._progress_bar.update_progress(self._times.current, simulation_time)
            log_network_state(self._times, self._servers)

            if self._times.current == self._times.arrival:
                self._demand_arrival()
                continue
            if self._times.current == self._times.service_start:
                self._demand_service_start()
                continue
            if self._times.current == self._times.leaving:
                self._demand_leaving()
                continue

        statistics.calculate_statistics(self._served_demands)
        return statistics

    def _demand_arrival(self) -> None:
        """Event describing the arrival of a demand to the system"""

        class_id = self._define_arriving_demand_class(self._first_class_arrival_probability)
        demand = Demand(self._times.arrival,
                        class_id, self._params.fragments_numbers[class_id])

        if len(self._queues[class_id]) < self._params.queues_capacities[class_id]:
            self._times.service_start = self._times.current
            self._queues[class_id].append(demand)
            log_arrival(demand, self._times.current)
        else:
            log_full_queue(demand, self._times.current)

        self._times.update_arrival_time(self._params.combined_lambda)

    def _demand_service_start(self) -> None:
        """Event describing the start of servicing a demand"""

        # take demand from queues according to certain policy
        while self._servers.can_any_class_occupy(self._params):
            class_id = self._selection_policy(self._get_current_state(), self._params)
            if self._queues[class_id] and self._servers.can_occupy(class_id, self._params):
                demand = self._queues[class_id].pop(0)
                self._servers.distribute_fragments(demand, self._times.current)
                self._demands_in_network.append(demand)
                demand.service_start_time = self._times.current
                log_service_start(demand, self._times.current)
            else:
                break

        self._times.service_start = float('inf')

        # take the near term of the end of servicing demands
        if self._servers.get_demands_ids_on_servers():
            self._times.leaving = self._servers.get_min_end_service_time_for_demand()

    def _demand_leaving(self) -> None:
        """Event describing a demand leaving the system"""

        leaving_demand_id = self._servers.get_demand_id_with_min_end_service_time()
        self._servers.to_free_demand_fragments(leaving_demand_id)
        demand = None

        for d in self._demands_in_network:
            if d.id == leaving_demand_id:
                demand = d
                self._demands_in_network.remove(demand)
                break

        demand.leaving_time = self._times.current
        self._served_demands.append(demand)
        self._set_events_times()

        log_leaving(demand, self._times.current)

    def _set_events_times(self) -> None:
        if self._servers.check_if_possible_put_demand_on_servers(self._params):
            self._times.service_start = self._times.current
        if not self._servers.get_demands_ids_on_servers():
            self._times.leaving = float('inf')
        else:
            self._times.leaving = self._servers.get_min_end_service_time_for_demand()

    def _get_current_state(self) -> list:
        return [len(self._queues[0]),
                len(self._queues[1]),
                self._servers.get_number_of_free_servers()]

    @staticmethod
    def _define_arriving_demand_class(probability: float) -> int:
        return 0 if random() < probability else 1
