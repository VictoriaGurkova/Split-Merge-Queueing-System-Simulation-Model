from SplitMerge import SplitMerge
from Statistics import Statistics

if __name__ == '__main__':
    simulation_time = 100000
    la1 = 0.5
    la2 = 1
    mu = 3
    M = 4
    list_of_fragments = [3, 2]
    capacity = [10, 30]

    statistics = Statistics(list_of_fragments)
    sp = SplitMerge(la1, la2,
                    mu, M,
                    list_of_fragments, capacity,
                    statistics)

    sp.main(simulation_time)
    statistics.show()
