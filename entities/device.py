from random import expovariate

from entities.fragment import Fragment


class Device:
    """The class describes the servicing device essence in a queuing network."""

    __COUNT = 0

    def __init__(self, mu: float):
        """

        :param mu: demand service rate
        """
        Device.__COUNT += 1
        self.id = Device.__COUNT
        self.fragment = None
        self.is_free = True
        self.mu = mu
        self.end_service_time = float('-inf')

    def to_occupy(self, fragment: Fragment, current_time: float):
        """The function describes fragment placing on the servicing device.

        :param fragment: fragment of the demand placed on the device
        :param current_time: current simulation time
        """
        self.is_free = False
        self.fragment = fragment
        self.end_service_time = current_time + expovariate(self.mu)

    def to_free(self):
        """The function describes completing fragment servicing."""

        self.is_free = True
        self.fragment = None
        self.end_service_time = float('-inf')
