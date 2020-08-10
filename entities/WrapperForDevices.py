from entities.Demand import Demand
from entities.Device import Device


class WrapperForDevices:
    """Wrapper class for grouping service devices.

    Contains auxiliary functionality for working with devices

    """

    def __init__(self, mu: float, amount_of_devices: int):
        """

        :param mu: demand service rate
        :param amount_of_devices: number of service devices
        """
        self.mu = mu
        self.list_of_devices = [Device(self.mu) for _ in range(amount_of_devices)]

    def distribute_fragments(self, demand: Demand, current_time: float):
        """Distributes fragments of a demand by devices.

        :param demand: demand, fragments of which must be assigned to devices
        :param current_time: current simulation time of the model
        """
        count = 0
        # scatter fragments over the devices
        for device in self.list_of_devices:
            if device.is_free and count < demand.amount_of_fragments:
                device.to_occupy(demand.list_of_fragments[count], current_time)
                count += 1

    def get_amount_of_free_devices(self):
        """Returns the number of free devices.

        :return: int
        """
        return len([True for device in self.list_of_devices if device.is_free])

    # возвращает ближайшее время окончания обслуживания требования
    def get_min_end_service_time_for_demand(self):
        """Returns the near term of the end of service of the claim.

        :return: float
        """
        lists_of_service_duration_fragments = self.get_lists_of_service_duration_fragments()
        # list of service times for all demands on devices at the moment
        max_service_duration_of_fragments = []

        for duration in lists_of_service_duration_fragments:
            max_service_duration_of_fragments.append(max(duration))

        return min(max_service_duration_of_fragments)

    def get_lists_of_service_duration_fragments(self):
        """Returns a list of lists of durations of servicing fragments of each demand in the network.

        :return: list
        """
        list_demands_on_devices = self.get_id_demands_on_devices()
        lists_of_service_duration_fragments = [[] for _ in range(len(list_demands_on_devices))]

        for id_demand in list_demands_on_devices:
            for device in self.list_of_devices:
                if not device.is_free and device.fragment.parent_id == id_demand:
                    lists_of_service_duration_fragments[list_demands_on_devices.index(id_demand)] \
                        .append(device.service_duration)

        return lists_of_service_duration_fragments

    def get_id_demands_on_devices(self):
        """Returns a list containing all demand ids on devices at the moment.

        :return: list
        """
        id_demands_on_devices = set()

        for device in self.list_of_devices:
            if not device.is_free:
                id_demands_on_devices.add(device.fragment.parent_id)

        return list(id_demands_on_devices)

    def get_id_demand_with_min_end_service_time(self):
        """Returns the id of the request with the closest service completion time.

        :return: int
        """
        for device in self.list_of_devices:
            if device.service_duration == self.get_min_end_service_time_for_demand():
                return device.fragment.parent_id

    def to_free_demand_fragments(self, demand_id: int):
        """The function frees devices from fragments of a demand that leaves the system.

        :param demand_id: id of the demand from which you want to release devices
        """
        for device in self.list_of_devices:
            if not device.is_free and device.fragment.parent_id == demand_id:
                device.to_free()
