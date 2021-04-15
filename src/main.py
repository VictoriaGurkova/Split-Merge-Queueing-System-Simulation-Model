from network_params import Params
from network_simulation import SplitMergeSystem
from progress_bar import ConsoleProgressBar
from src.selection_policy import SelectionPolicy

if __name__ == '__main__':
    # this code initializes network parameters, starts statistics and performs simulation split-merge network
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=5,
                    fragments_numbers=[2, 3],
                    queues_capacities=[1, 1])
    bar = ConsoleProgressBar('Progress: ')



    model = SplitMergeSystem(params, bar, SelectionPolicy.random)

    simulation_time = 100_000
    statistics = model.run(simulation_time)

    print(statistics)
