from SplitMerge import SplitMerge
from Statistics import Statistics


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    simulation_time = 100000
    lambda1 = 0.5
    lambda2 = 1
    mu = 3
    M = 4
    fragments_of_demands = [3, 2]
    dimension_of_queues = [10, 30]

    statistics = Statistics(fragments_of_demands)
    network_model = SplitMerge(lambda1, lambda2,
                               mu, M,
                               fragments_of_demands, dimension_of_queues,
                               statistics)

    network_model.main(simulation_time)
    statistics.show()
