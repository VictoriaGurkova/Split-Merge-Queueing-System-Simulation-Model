from entities.demand import Demand
from entities.server import Server
from network_params import Params


class ServersWrapper:
    """This class contains auxiliary functions for working with servers."""

    def __init__(self, mu: float, servers_number: int) -> None:
        """
        @param mu: demand service rate
        @param servers_number: number of servicing servers
        """
        self.mu = mu
        self.servers = [Server(self.mu) for _ in range(servers_number)]

    def distribute_fragments(self, demand: Demand, current_time: float) -> None:
        """The function distributes a demand fragments by servers.

        @param demand: demand, fragments of which must be assigned to servers
        @param current_time: current simulation time of the model
        """
        count = 0
        # distributing fragments over the servers
        for server in self.servers:
            if server.is_free and count < demand.fragments_number:
                server.to_occupy(demand.fragments[count], current_time)
                count += 1

    def get_number_of_free_servers(self) -> int:
        """The function returns the number of free servers."""
        return len([True for server in self.servers if server.is_free])

    def get_min_end_service_time_for_demand(self) -> float:
        """The function returns the near term of the end of service of the claim."""
        service_duration_fragments = self.get_fragments_service_durations()
        # list of service times for all demands on servers at the moment
        max_service_duration = []

        for duration in service_duration_fragments:
            max_service_duration.append(max(duration))

        return min(max_service_duration)

    def get_fragments_service_durations(self) -> list:
        """The function returns a list of lists of each demand fragments servicing durations in the network."""
        demands_on_servers = self.get_demands_ids_on_servers()
        lists_of_fragments_service_durations = [[] for _ in range(len(demands_on_servers))]

        for demand_id in demands_on_servers:
            for server in self.servers:
                if not server.is_free and server.fragment.parent_id == demand_id:
                    lists_of_fragments_service_durations[demands_on_servers.index(demand_id)] \
                        .append(server.end_service_time)

        return lists_of_fragments_service_durations

    def get_demands_ids_on_servers(self) -> list:
        """The function returns a list containing all demand ids on servers at the moment."""
        demands_ids_on_servers = set()

        for server in self.servers:
            if not server.is_free:
                demands_ids_on_servers.add(server.fragment.parent_id)

        return list(demands_ids_on_servers)

    def get_demand_id_with_min_end_service_time(self) -> int:
        """The function returns the demand id with the closest service completion time."""
        min_end_service_time = self.get_min_end_service_time_for_demand()
        for server in self.servers:
            if server.end_service_time == min_end_service_time:
                return server.fragment.parent_id

    def to_free_demand_fragments(self, demand_id: int) -> None:
        """The function frees servers from demand fragments leaving the system.

        @param demand_id: demand id which have to release servers
        """
        for server in self.servers:
            if not server.is_free and server.fragment.parent_id == demand_id:
                server.to_free()

    def can_any_class_occupy(self, params: Params) -> bool:
        classes_number = len(params.fragments_numbers)
        can_occupy_systems = False
        for i in range(classes_number):
            can_occupy_systems = self.can_occupy(i, params)
        return can_occupy_systems

    def can_occupy(self, class_id: int, params: Params) -> bool:
        """The function checks if the this class demand can service on the servers.

        @param params: network configuration parameters
        @param class_id: demand class
        """
        return self.get_number_of_free_servers() >= params.fragments_numbers[class_id]

    def check_if_possible_put_demand_on_servers(self, params: Params) -> bool:
        """The function checks if it is possible to put a demand on servers."""
        return bool([True for class_id in range(len(params.fragments_numbers))
                    if self.can_occupy(class_id, params)])
