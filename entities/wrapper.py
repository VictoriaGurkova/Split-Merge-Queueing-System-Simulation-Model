from entities.demand import Demand
from entities.device import Device
from network_params import Params


class DevicesWrapper:
    """This class contains auxiliary functions for working with devices."""

    def __init__(self, mu: float, amount_of_devices: int):
        """
        :param mu: demand service rate
        :param amount_of_devices: number of servicing devices
        """
        self.mu = mu
        self.devices = [Device(self.mu) for _ in range(amount_of_devices)]

    def distribute_fragments(self, demand: Demand, current_time: float):
        """It distributes a demand fragments by devices.

        :param demand: demand, fragments of which must be assigned to devices
        :param current_time: current simulation time of the model
        """
        count = 0
        # scatter fragments over the devices
        for device in self.devices:
            if device.is_free and count < demand.fragments_amount:
                device.to_occupy(demand.fragments[count], current_time)
                count += 1

    def get_amount_of_free_devices(self):
        """Returns the number of free devices.

        :return: int
        """
        return len([True for device in self.devices if device.is_free])

    def get_min_end_service_time_for_demand(self):
        """Returns the near term of the end of service of the claim.

        :return: float
        """
        service_duration_fragments = self.get_service_duration_fragments()
        # list of service times for all demands on devices at the moment
        max_service_duration = []

        for duration in service_duration_fragments:
            max_service_duration.append(max(duration))

        return min(max_service_duration)

    def get_service_duration_fragments(self):
        """Returns a list of lists of durations of servicing fragments of each demand in the network.

        :return: list
        """
        demands_on_devices = self.get_id_demands_on_devices()
        lists_of_service_duration_fragments = [[] for _ in range(len(demands_on_devices))]

        for demand_id in demands_on_devices:
            for device in self.devices:
                if not device.is_free and device.fragment.parent_id == demand_id:
                    lists_of_service_duration_fragments[demands_on_devices.index(demand_id)] \
                        .append(device.service_duration)

        return lists_of_service_duration_fragments

    def get_id_demands_on_devices(self):
        """Returns a list containing all demand ids on devices at the moment.

        :return: list
        """
        demands_id_on_devices = set()

        for device in self.devices:
            if not device.is_free:
                demands_id_on_devices.add(device.fragment.parent_id)

        return list(demands_id_on_devices)

    def get_demand_id_with_min_end_service_time(self):
        """Returns the id of the request with the closest service completion time.

        :return: int
        """
        min_end_service_time = self.get_min_end_service_time_for_demand()
        for device in self.devices:
            if device.service_duration == min_end_service_time:
                return device.fragment.parent_id

    def to_free_demand_fragments(self, demand_id: int):
        """The function frees devices from fragments of a demand that leaves the system.

        :param demand_id: id of the demand from which you want to release devices
        """
        for device in self.devices:
            if not device.is_free and device.fragment.parent_id == demand_id:
                device.to_free()

    def can_occupy(self, class_id: int, params: Params):
        """Checking whether the demand of this class can take place on the devices

        :param params: network configuration parameters
        :param class_id: demand class
        """
        return self.get_amount_of_free_devices() >= params.fragments_amounts[class_id]

    def check_if_possible_put_demand_on_devices(self, params: Params):
        """Checking whether it is possible to place a demand on devices"""
        return len([True for class_id in range(len(params.fragments_amounts))
                    if self.can_occupy(class_id, params)])

