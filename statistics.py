import matplotlib.pyplot as plt
from pprint import pprint


# TODO: make clean
class Statistics:

    def __init__(self, fragments_amounts: list):
        self.classes_amount = len(fragments_amounts)
        self.demands_amount = 0
        self.responses = []
        self.general_stat = {
            "demands_amount": 0,
            "average_response_time": 0,
            "average_time_in_queue": 0,
            "average_time_on_device": 0
        }
        self.class_statistics = {
            f"class_{i}": self.general_stat.copy() for i in range(self.classes_amount)
        }

    def record(self, demands: list):
        self.general_stat["demands_amount"] = len(demands)
        for demand in demands:
            self.responses.append(demand.leaving_time - demand.arrival_time)
            self.general_stat["average_response_time"] += demand.leaving_time - demand.arrival_time
            self.general_stat["average_time_in_queue"] += demand.service_start_time - demand.arrival_time
            self.general_stat["average_time_on_device"] += demand.leaving_time - demand.service_start_time
        self.general_stat["average_response_time"] /= self.general_stat["demands_amount"]
        self.general_stat["average_time_in_queue"] /= self.general_stat["demands_amount"]
        self.general_stat["average_time_on_device"] /= self.general_stat["demands_amount"]

        for i in range(self.classes_amount):
            for demand in demands:
                if demand.class_id == i:
                    self.class_statistics[f"class_{i}"]["demands_amount"] += 1
                    self.class_statistics[f"class_{i}"]["average_response_time"] += \
                        demand.leaving_time - demand.arrival_time
                    self.class_statistics[f"class_{i}"]["average_time_in_queue"] += \
                        demand.service_start_time - demand.arrival_time
                    self.class_statistics[f"class_{i}"]["average_time_on_device"] += \
                        demand.leaving_time - demand.service_start_time

        for i in range(self.classes_amount):
            self.class_statistics[f"class_{i}"]["average_response_time"] /= \
                self.class_statistics[f"class_{i}"]["demands_amount"]
            self.class_statistics[f"class_{i}"]["average_time_in_queue"] /= \
                self.class_statistics[f"class_{i}"]["demands_amount"]
            self.class_statistics[f"class_{i}"]["average_time_on_device"] /= \
                self.class_statistics[f"class_{i}"]["demands_amount"]

    def show(self):
        print("\nСтатистика для всех требований:")
        pprint(self.general_stat)
        print("Статистика по классам требований:")
        pprint(self.class_statistics)
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

    def __init__(self):
        pass

    def record(self, demands):
        pass

    def show(self):
        pass
