import logging
from random import expovariate as exp, random

from network_params import Params
from progress_bar import ProgressBar
from statistics import Statistics
from entities.wrapper import DevicesWrapper
from entities.demand import Demand


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

        logging.basicConfig(filename="logging.log", level=logging.ERROR, filemode="w")

        self.params = params
        self.statistics = statistics

        self.lambdas = {
            "lambda1": params.lambda1,
            "lambda2": params.lambda2,
            "lambda": params.lambda1 + params.lambda2
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

        class_id = self.define_arriving_demand_class()
        demand = Demand(self.times["arrival"], class_id, self.params.fragments_amounts[class_id])

        if len(self.config["queues"][class_id]) < self.params.queues_capacities[class_id]:
            self.times["service_start"] = self.times["current"]
            self.config["queues"][class_id].append(demand)

            logging.debug("Demand arrival: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                          ". Current Time: " + str(self.times["current"]))
        else:
            logging.debug(
                "Demand arrival (FULL QUEUE): ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                ". Current Time: " + str(self.times["current"]))

        self.times["arrival"] += exp(self.lambdas["lambda"])

    def demand_service_start(self):
        """Event describing the start of servicing a demand"""

        # take demand from all queues in direct order
        for class_id in range(len(self.params.fragments_amounts)):
            while self.can_occupy(class_id) and self.config["queues"][class_id]:
                demand = self.config["queues"][class_id].pop(0)
                self.config["devices"].distribute_fragments(demand, self.times["current"])
                self.stat["demands_in_network"].append(demand)
                demand.service_start_time = self.times["current"]

                logging.debug("Demand start service: ID - " + str(demand.id) + ". Class ID - " +
                              str(demand.class_id) + ". Current Time: " + str(self.times["current"]))

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
        self.set_events_times()

        logging.debug("Demand leaving: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                      ". Current Time: " + str(self.times["current"]))

    def define_arriving_demand_class(self):
        return 0 if random() < self.prob1 else 1

    def set_events_times(self):
        if self.check_if_possible_put_demand_on_devices():
            self.times["service_start"] = self.times["current"]
        if not self.config["devices"].get_id_demands_on_devices():
            self.times["leaving"] = float('inf')
        else:
            self.times["leaving"] = self.config["devices"].get_min_end_service_time_for_demand()

    def can_occupy(self, class_id: int):
        """Checking whether the demand of this class can take place on the devices

        :param class_id: demand class
        """
        return self.config["devices"].get_amount_of_free_devices() >= self.params.fragments_amounts[class_id]

    def check_if_possible_put_demand_on_devices(self):
        """Checking whether it is possible to place a demand on devices"""

        return len([True for class_id in range(len(self.params.fragments_amounts))
                    if self.can_occupy(class_id)])

    def imitation(self, simulation_time: int):
        """

        :param simulation_time: model simulation duration
        """

        bar = ProgressBar(0, 'Progress: ')

        while self.times["current"] <= simulation_time:
            self.times["current"] = min(self.times["arrival"], self.times["service_start"], self.times["leaving"])

            bar.print_progress(self.times["current"], simulation_time)

            logging.debug("Device's state: " + str(self.config["devices"].get_id_demands_on_devices()))
            logging.debug("Device's state with min time: " +
                          str(self.config["devices"].get_service_duration_fragments()))
            logging.debug("Event times: = " +
                          str([self.times["arrival"], self.times["service_start"], self.times["leaving"]]))

            if self.times["current"] == self.times["arrival"]:
                self.arrival_of_demand()
                continue
            if self.times["current"] == self.times["service_start"]:
                self.demand_service_start()
                continue
            if self.times["current"] == self.times["leaving"]:
                self.leaving_demand()
                continue

        print()
        self.statistics.record(self.stat["served_demands"])
