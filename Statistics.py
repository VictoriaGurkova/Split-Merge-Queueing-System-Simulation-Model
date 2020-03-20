from pprint import pprint
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, list_amounts_of_fragments: list):
        self._amount_of_classes = len(list_amounts_of_fragments)
        self._list_of_responses = []
        self._general_statistics = {
            "amount_of_demands": 0,
            "average_response_time": 0,
            "average_time_in_queue": 0,
            "average_time_on_device": 0
        }
        self._class_statistics = {
            f"class_{i}": self._general_statistics.copy() for i in range(self._amount_of_classes)
        }

    def record(self, list_of_demands: list):
        for demand in list_of_demands:
            self._list_of_responses.append(demand.leaving_time - demand.arrival_time)
            self._general_statistics["amount_of_demands"] += 1
            self._general_statistics["average_response_time"] += demand.leaving_time - demand.arrival_time
            self._general_statistics["average_time_in_queue"] += demand.service_start_time - demand.arrival_time
            self._general_statistics["average_time_on_device"] += demand.leaving_time - demand.service_start_time
        self._general_statistics["average_response_time"] /= self._general_statistics["amount_of_demands"]
        self._general_statistics["average_time_in_queue"] /= self._general_statistics["amount_of_demands"]
        self._general_statistics["average_time_on_device"] /= self._general_statistics["amount_of_demands"]

        for i in range(self._amount_of_classes):
            for demand in list_of_demands:
                if demand.class_id == i:
                    self._class_statistics[f"class_{i}"]["amount_of_demands"] += 1
                    self._class_statistics[f"class_{i}"]["average_response_time"] += \
                        demand.leaving_time - demand.arrival_time
                    self._class_statistics[f"class_{i}"]["average_time_in_queue"] += \
                        demand.service_start_time - demand.arrival_time
                    self._class_statistics[f"class_{i}"]["average_time_on_device"] += \
                        demand.leaving_time - demand.service_start_time

        for i in range(self._amount_of_classes):
            self._class_statistics[f"class_{i}"]["average_response_time"] /= \
                self._class_statistics[f"class_{i}"]["amount_of_demands"]
            self._class_statistics[f"class_{i}"]["average_time_in_queue"] /= \
                self._class_statistics[f"class_{i}"]["amount_of_demands"]
            self._class_statistics[f"class_{i}"]["average_time_on_device"] /= \
                self._class_statistics[f"class_{i}"]["amount_of_demands"]

    def show(self):
        print("Статистика для всех требований:")
        pprint(self._general_statistics)
        print("Статистика по классам требований:")
        pprint(self._class_statistics)
        fig, (ax1, ax2) = plt.subplots(
            nrows=1, ncols=2,
            figsize=(20, 10)
        )
        ax1.plot(self._list_of_responses)
        ax1.set_xlabel("Количество требований")
        ax1.set_ylabel("Длительность пребывания в сети")

        ax2.hist(self._list_of_responses)
        ax2.set_xlabel("Длительность пребывания в сети")
        ax2.set_ylabel("Количество требований")

        plt.show()

