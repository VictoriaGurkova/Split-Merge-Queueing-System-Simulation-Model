from random import expovariate


class Device:
    count = 0

    def __init__(self, mu):
        Device.count += 1
        self.id = Device.count
        self.fragment = None
        self.is_free = True
        self.mu = mu
        self.service_duration = float('-inf')

    def to_occupy(self, fragment):
        self.is_free = False
        self.fragment = fragment
        self.service_duration = expovariate(self.mu)

    def to_free(self):
        self.is_free = True
        self.fragment = None
        self.service_duration = float('-inf')
