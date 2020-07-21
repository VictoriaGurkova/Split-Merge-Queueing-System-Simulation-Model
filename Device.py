from random import expovariate

from Fragment import Fragment


class Device:
    count = 0

    def __init__(self, mu: float):
        Device.count += 1
        self.id = Device.count
        self.fragment = None
        self.is_free = True
        self.mu = mu
        self.service_duration = float('-inf')

    def to_occupy(self, fragment: Fragment, current_time: float):
        self.is_free = False
        self.fragment = fragment
        self.service_duration = current_time + expovariate(self.mu)

    def to_free(self):
        self.is_free = True
        self.fragment = None
        self.service_duration = float('-inf')
