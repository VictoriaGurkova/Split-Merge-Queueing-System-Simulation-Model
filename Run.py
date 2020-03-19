from Split_Merge import SplitMerge
from Statistics import Statistics

if __name__ == '__main__':
    simulation_time = 100000
    la = 0.5
    mu = 1
    M = 4
    list_of_fragments = [1, 2]
    statistics = Statistics(list_of_fragments)
    sp = SplitMerge(la, mu, M, list_of_fragments, statistics)

    sp.main(simulation_time)
    statistics.show()
