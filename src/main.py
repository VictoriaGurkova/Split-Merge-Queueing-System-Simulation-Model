from network_simulation import SplitMergeSystem
from network_params import Params
from progress_bar import ConsoleProgressBar


# this code initializes network parameters, starts statistics and performs simulation split-merge network
from src.selection_policy import SelectionPolicy

if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=5,
                    fragments_numbers=[2, 3],
                    queues_capacities=[10, 10])
    bar = ConsoleProgressBar('Progress: ')

    model = SplitMergeSystem(params, bar, SelectionPolicy.direct_order)

    simulation_time = 100000
    statistics = model.run(simulation_time)

    print(statistics)
