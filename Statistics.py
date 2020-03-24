from statistics import mean
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, list_amounts_of_fragments: list):
        self._amount_of_classes = len(list_amounts_of_fragments)
        self._list_of_responses = []  # время пребывания требований в системе
        self._list_time_in_queue = []  # время пребывания требований в очереди
        self._list_time_on_device = []  # время пребывания требований на приборе
        self._list_for_classes = []

    def _record_classes(self, list_of_demands: list):
        for i in range(self._amount_of_classes):
            self._list_for_classes.append([])
            for demand in list_of_demands:
                if demand.class_id == i:
                    self._list_for_classes[i].append(demand.leaving_time - demand.arrival_time)

    def record(self, list_of_demands: list):
        self._record_classes(list_of_demands)
        for demand in list_of_demands:
            self._list_of_responses.append(demand.leaving_time - demand.arrival_time)
            self._list_time_in_queue.append(demand.service_start_time - demand.arrival_time)
            self._list_time_on_device.append(demand.leaving_time - demand.service_start_time)

    def show(self):
        print("Статистика для всех требований:")
        print("М.о. длительности пребывания требования в сети:", mean(self._list_of_responses))
        print("М.о. длительности пребывания требования в очереди:", mean(self._list_time_in_queue))
        print("М.о. длительности пребывания требования на приборе", mean(self._list_time_on_device))

        plt.title("В сети")
        plt.xlabel("Количество требования")
        plt.ylabel("Длительность пребывания")
        plt.plot(self._list_of_responses, "b")
        plt.show()

        plt.title("В очередях")
        plt.xlabel("Количество требования")
        plt.ylabel("Длительность пребывания")
        plt.plot(self._list_time_in_queue, "r")
        plt.show()

        plt.title("На приборах")
        plt.xlabel("Количество требования")
        plt.ylabel("Длительность пребывания")
        plt.plot(self._list_time_on_device, "g")
        plt.show()

        print()

        for class_list in self._list_for_classes:
            print(f"М.о. длительности пребывания требования {self._list_for_classes.index(class_list)} класса в сети:",
                  mean(class_list))
            plt.title(f"В сети ({self._list_for_classes.index(class_list)} класс требований)")
            plt.xlabel("Количество требования")
            plt.ylabel("Длительность пребывания")
            plt.plot(class_list, "b")
            plt.show()



