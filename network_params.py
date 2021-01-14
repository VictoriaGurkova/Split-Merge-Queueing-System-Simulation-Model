class Params:

    def __init__(self, lambda1: float, lambda2: float, mu: float,
                 devices_amount: int, fragments_amounts: list,
                 queues_capacities: list):
        """
        :param lambda1: intensity of the incoming flow of first class demand
        :param lambda2: intensity of the incoming flow of second class demand
        :param mu: service rate of a demand by one device
        :param devices_amount: number of devices in the system
        :param fragments_amounts: view [a, b], where a is the number of fragments of the first class demand
        and b - second demand
        :param queues_capacities: queue dimensions, similarly as list_amounts_of_fragments
        """
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.devices_amount = devices_amount
        self.fragments_amounts = fragments_amounts
        self.queues_capacities = queues_capacities
