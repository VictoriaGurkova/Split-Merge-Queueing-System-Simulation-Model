class Params:
    # TODO: убарть все аргументы по умолчанию
    # TODO: преобразовать в дата-класс?
    def __init__(self, lambda1=.5, lambda2=1, mu=3,
                 devices_amount=4, fragments_amounts=None,
                 queues_capacities=None):
        """
        :param lambda1: intensity of the incoming flow of first class demand, default value = 0,5
        :param lambda2: intensity of the incoming flow of second class demand, default value = 1
        :param mu: service rate of a demand by one device, default value = 3
        :param devices_amount: number of devices in the system, default value = 4
        :param fragments_amounts: view [a, b], where a is the number of fragments of the first class demand
        a and b - second demand, default value = [a=3, b=2]
        :param queues_capacities: queue dimensions, similarly as list_amounts_of_fragments, default value = [10, 30]
        """
        # TODO: убрать
        if fragments_amounts is None:
            fragments_amounts = [3, 2]
        if queues_capacities is None:
            queues_capacities = [10, 30]

        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.devices_amount = devices_amount
        self.fragments_amounts = fragments_amounts
        self.queues_capacities = queues_capacities

    def get_lambda(self):
        return self.lambda1 + self.lambda2
