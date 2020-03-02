class Device:
    count = 0

    def __init__(self, mu):
        Device.count += 1
        self.id = Device.count
        self.fragment = None
        # false - прибор свободен; true - прибор занят
        self.service_flag = False
        self.mu = mu

    def to_occupy(self, fragment):
        self.service_flag = True
        self.fragment = fragment

    def to_free(self):
        self.service_flag = False
        self.fragment = None

    def get_fragment(self):
        return self.fragment
