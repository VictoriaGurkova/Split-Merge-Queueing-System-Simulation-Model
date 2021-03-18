from random import expovariate

from src.entities.fragment import Fragment


class Server:
    """The class describes the server essence in a queuing network."""

    __COUNT = 0

    def __init__(self, mu: float) -> None:
        """

        @param mu: demand service rate
        """
        Server.__COUNT += 1
        self.id = Server.__COUNT
        self.fragment = None
        self.is_free = True
        self.mu = mu
        self.end_service_time = float('-inf')

    def to_occupy(self, fragment: Fragment, current_time: float) -> None:
        """The function describes fragment placing on the server.

        @param fragment: fragment of the demand placed on the server
        @param current_time: current simulation time
        """
        self.is_free = False
        self.fragment = fragment
        self.end_service_time = current_time + expovariate(self.mu)

    def to_free(self) -> None:
        """The function describes completing fragment servicing."""

        self.is_free = True
        self.fragment = None
        self.end_service_time = float('-inf')
