from dataclasses import dataclass

import matplotlib.pyplot as plt


class Statistics:

    def __init__(self, fragments_amounts: list) -> None:
        self.classes_amount = len(fragments_amounts)
        self.responses = []
        self.total_statistics = StatisticalFields()
        self.class_statistics = [ClassStatistics(class_id) for class_id in range(len(fragments_amounts))]

    def calculate_statistics(self, demands: list) -> None:
        self._calculate_total_statistics(demands)
        for cs in self.class_statistics:
            cs.calculate_class_statistics(demands)

    def _calculate_total_statistics(self, demands: list) -> None:
        self.total_statistics.demands_amount = len(demands)
        calculate(demands, self.total_statistics)
        for demand in demands:
            self.responses.append(demand.leaving_time - demand.arrival_time)

    # TODO: зачем? куда?
    def draw_plot(self):
        fig, (ax1, ax2) = plt.subplots(
            nrows=1, ncols=2,
            figsize=(20, 10)
        )
        ax1.plot(self.responses)
        ax1.set_xlabel("Количество требований")
        ax1.set_ylabel("Длительность пребывания в сети")

        ax2.hist(self.responses)
        ax2.set_xlabel("Длительность пребывания в сети")
        ax2.set_ylabel("Количество требований")

        plt.show()

    def __str__(self) -> str:
        s = f"\ntotal statistics:\n{self.total_statistics}\n"
        for cs in self.class_statistics:
            s += f"\n{cs}"
        return s


class ClassStatistics:

    def __init__(self, class_id: int) -> None:
        self.class_id = class_id
        self.demands = None
        self.statistics = StatisticalFields()

    def calculate_class_statistics(self, demands: list) -> None:
        self.demands = [demand for demand in demands if demand.class_id == self.class_id]
        self.statistics.demands_amount = len(self.demands)
        calculate(self.demands, self.statistics)

    def __str__(self) -> str:
        return f"class id: {self.class_id} -> \n\t{self.statistics}\n"


@dataclass
class StatisticalFields:
    demands_amount: int = 0
    avg_response_time: float = 0
    avg_time_in_queue: float = 0
    avg_time_on_device: float = 0


def calculate(demands: list, statistics: StatisticalFields) -> None:
    for demand in demands:
        statistics.avg_response_time += demand.leaving_time - demand.arrival_time
        statistics.avg_time_in_queue += demand.service_start_time - demand.arrival_time
        statistics.avg_time_on_device += demand.leaving_time - demand.service_start_time
    statistics.avg_response_time /= statistics.demands_amount
    statistics.avg_time_in_queue /= statistics.demands_amount
    statistics.avg_time_on_device /= statistics.demands_amount


if __name__ == '__main__':
    sf = StatisticalFields()
    print(sf)
