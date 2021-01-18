from random import expovariate as exp

from entities.demand import Demand
from entities.wrapper import DevicesWrapper
from logs import *
from progress_bar import ProgressBar
from statistics import Statistics
from utils import *


class SplitMergeSystem:
    """Class describing the simulation model split-merge simulation model of a queuing system

    Two classes of demand, two queues for demand.
    The progression of simulation time is from event to event.
    Events: arrival demand, start service demand and leaving demand

    """

    def __init__(self,
                 params: Params,
                 statistics: Statistics):
        """

        :param params: network configuration parameters
        :param statistics: variable for counting and calculating statistics

        """

        self.params = params
        self.statistics = statistics

        self.lambdas = {
            "lambda1": params.lambda1,
            "lambda2": params.lambda2,
            "lambda": params.get_lambda()
        }
        self.prob1 = self.lambdas["lambda1"] / self.lambdas["lambda"]

        self.times = {
            "current": 0,
            "arrival": exp(self.lambdas["lambda"]),
            "service_start": float('inf'),
            "leaving": float('inf')
        }

        # network configuration - number of queues and devices
        self.config = {
            "queues": list([] for _ in range(len(params.fragments_amounts))),  # view: [[], []]
            "devices": DevicesWrapper(params.mu, params.devices_amount)
        }

        # data for calculating statistics
        self.stat = {
            "demands_in_network": [],
            "served_demands": []
        }

    def arrival_of_demand(self):
        """Event describing the arrival of a demand to the system"""

        class_id = define_arriving_demand_class(self.prob1)
        demand = Demand(self.times["arrival"], class_id, self.params.fragments_amounts[class_id])

        if len(self.config["queues"][class_id]) < self.params.queues_capacities[class_id]:
            self.times["service_start"] = self.times["current"]
            self.config["queues"][class_id].append(demand)
            log_arrival(demand, self.times["current"])
        else:
            log_full_queue(demand, self.times["current"])

        self.times["arrival"] += exp(self.lambdas["lambda"])

    def demand_service_start(self):
        """Event describing the start of servicing a demand"""

        # take demand from all queues in direct order
        for class_id in range(len(self.params.fragments_amounts)):
            while self.config["devices"].can_occupy(class_id, self.params) and self.config["queues"][class_id]:
                demand = self.config["queues"][class_id].pop(0)
                self.config["devices"].distribute_fragments(demand, self.times["current"])
                self.stat["demands_in_network"].append(demand)
                demand.service_start_time = self.times["current"]
                log_service_start(demand, self.times["current"])

        self.times["service_start"] = float('inf')

        # take the near term of the end of servicing demands
        if self.config["devices"].get_id_demands_on_devices():
            self.times["leaving"] = self.config["devices"].get_min_end_service_time_for_demand()

    def leaving_demand(self):
        """Event describing a demand leaving the system"""

        leaving_demand_id = self.config["devices"].get_demand_id_with_min_end_service_time()
        self.config["devices"].to_free_demand_fragments(leaving_demand_id)
        demand = None

        for d in self.stat["demands_in_network"]:
            if d.id == leaving_demand_id:
                demand = d
                self.stat["demands_in_network"].remove(demand)
                break

        demand.leaving_time = self.times["current"]
        self.stat["served_demands"].append(demand)
        set_events_times(self.times, self.config, self.params)

        log_leaving(demand, self.times["current"])

    def imitation(self, simulation_time: int):
        """

        :param simulation_time: model simulation duration
        """

        bar = ProgressBar(0, 'Progress: ')

        while self.times["current"] <= simulation_time:
            self.times["current"] = min(self.times["arrival"], self.times["service_start"], self.times["leaving"])

            bar.print_progress(self.times["current"], simulation_time)
            log_network_state(self.times, self.config["devices"])

            if self.times["current"] == self.times["arrival"]:
                self.arrival_of_demand()
                continue
            if self.times["current"] == self.times["service_start"]:
                self.demand_service_start()
                continue
            if self.times["current"] == self.times["leaving"]:
                self.leaving_demand()
                continue

        self.statistics.calculate_stat(self.stat["served_demands"])
