from network import SplitMergeSystem
from statistics import Statistics


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    simulation_time = 100000
    lambda1 = 0.5
    lambda2 = 1
    mu = 3
    M = 4
    demands_fragments = [3, 2]
    queues_capacity = [10, 30]

    statistics = Statistics(demands_fragments)
    network_model = SplitMergeSystem(lambda1, lambda2,
                                     mu, M,
                                     demands_fragments, queues_capacity,
                                     statistics)

    network_model.main(simulation_time)
    statistics.show()
