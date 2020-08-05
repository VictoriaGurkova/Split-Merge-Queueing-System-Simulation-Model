from random import expovariate

from entities.Fragment import Fragment


class Device:
    """Class describing the essence of a service device in a queuing network."""

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
        self.service_duration = float('-inf')

    def to_occupy(self, fragment: Fragment, current_time: float):
        """A function that describes placing a fragment on the device for servicing.

        :param fragment: fragment of the demand placed on the device
        :param current_time: current simulation time of the model
        """
        self.is_free = False
        self.fragment = fragment
        self.service_duration = current_time + expovariate(self.mu)

    def to_free(self):
        """Freeing the device from the fragment.(Completing a Fragment Service)"""

        self.is_free = True
        self.fragment = None
        self.service_duration = float('-inf')
