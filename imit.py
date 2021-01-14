from network import SplitMergeSystem
from network_params import Params
from statistics import Statistics


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    simulation_time = 100000

    params = Params()
    statistics = Statistics(params.fragments_amounts)

    model = SplitMergeSystem(params, statistics)
    model.imitation(simulation_time)

    statistics.show()
    # statistics.draw_plot()
