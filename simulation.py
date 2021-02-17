from network import SplitMergeSystem
from network_params import Params
from progress_bar import ConsoleProgressBar


# this code initializes network parameters, starts statistics and performs simulation split-merge network
if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    devices_amount=4,
                    fragments_amounts=[3, 2],
                    queues_capacities=[10, 30])
    bar = ConsoleProgressBar('Progress: ')

    model = SplitMergeSystem(params, bar)

    simulation_time = 100000
    statistics = model.run(simulation_time)

    # TODO: __str__
    statistics.show()
    # statistics.draw_plot()
