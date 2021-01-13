from network import SplitMergeSystem
from network_params import Params
from statistics import Statistics


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    simulation_time = 100000
    lambda1 = .5
    lambda2 = 1
    mu = 3
    devices_amount = 4
    fragments_amounts = [3, 2]
    queues_capacities = [10, 30]

    network_params = Params(lambda1, lambda2, mu, devices_amount, fragments_amounts, queues_capacities)
    statistics = Statistics(fragments_amounts)

    network_model = SplitMergeSystem(network_params, statistics)
    network_model.imitation(simulation_time)

    statistics.show()
