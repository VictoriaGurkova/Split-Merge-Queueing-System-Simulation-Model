from random import expovariate


class Device:
    count = 0

    def __init__(self, mu):
        Device.count += 1
        self.id = Device.count
        self.fragment = None
        # false - прибор свободен; true - прибор занят
        self.is_free = True
        self.mu = mu

    def to_occupy(self, fragment):
        self.is_free = False
        self.fragment = fragment

    def to_free(self):
        self.is_free = True
        self.fragment = None

    def get_fragment(self):
        return self.fragment

    def get_service_duration(self):
        return expovariate(self.mu)
