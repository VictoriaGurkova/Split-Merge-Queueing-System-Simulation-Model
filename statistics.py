import matplotlib.pyplot as plt
from pprint import pprint


# TODO: make clean
class Statistics:

    def __init__(self, fragments_amounts: list):
        self.classes_amount = len(fragments_amounts)
        self.responses = []

        self.statistics = {
            "demands_amount": 0,
            "avg_response_time": 0,
            "avg_time_in_queue": 0,
            "avg_time_on_device": 0
        }

        self.class_statistics = {
            f"class_{id}": ClassStatistics(id) for id in range(self.classes_amount)
        }

    def calculate_stat(self, demands: list):
        self.calculate_general_stat(demands)
        for class_stat in self.class_statistics.values():
            class_stat.calculate_class_stat(demands)

    def calculate_general_stat(self, demands):
        self.statistics["demands_amount"] = len(demands)
        calculate(demands, self.statistics)

        for demand in demands:
            self.responses.append(demand.leaving_time - demand.arrival_time)

    def show(self):
        print("\nСтатистика для всех требований:")
        pprint(self.statistics)

        print("Статистика по классам требований:")
        for class_stat in self.class_statistics.values():
            class_stat.show()

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


class ClassStatistics:

    def __init__(self, class_id: int):
        self.class_id = class_id
        self.demands = None
        self.statistics = {
            "demands_amount": 0,
            "avg_response_time": 0,
            "avg_time_in_queue": 0,
            "avg_time_on_device": 0
        }

    def calculate_class_stat(self, demands: list):
        self.demands = [demand for demand in demands if demand.class_id == self.class_id]
        self.statistics["demands_amount"] = len(self.demands)
        calculate(self.demands, self.statistics)

    def show(self):
        print("class id:", self.class_id)
        pprint(self.statistics)


def calculate(demands, statistics):
    for demand in demands:
        statistics["avg_response_time"] += demand.leaving_time - demand.arrival_time
        statistics["avg_time_in_queue"] += demand.service_start_time - demand.arrival_time
        statistics["avg_time_on_device"] += demand.leaving_time - demand.service_start_time
    statistics["avg_response_time"] /= statistics["demands_amount"]
    statistics["avg_time_in_queue"] /= statistics["demands_amount"]
    statistics["avg_time_on_device"] /= statistics["demands_amount"]