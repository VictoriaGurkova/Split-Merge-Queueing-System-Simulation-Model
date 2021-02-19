from network import SplitMergeSystem
from network_params import Params
from progress_bar import ConsoleProgressBar


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=4,
                    fragments_numbers=[3, 2],
                    queues_capacities=[10, 30])
    bar = ConsoleProgressBar('Progress: ')

    model = SplitMergeSystem(params, bar)

    simulation_time = 10000
    statistics = model.run(simulation_time)

    print(statistics)
    # statistics.draw_plot()
