from Device import Device


# класс-обертка для приборов
# содержит некоторые вспомогательные методы
class Wrapper_for_Devices:
    def __init__(self, mu, amount_of_devices):
        self.mu = mu
        # генерируется список amount_of_devices приборов с интенсивностями mu
        self.list_of_devices = [Device(self.mu) for _ in range(amount_of_devices)]
        # список для хранения длительностей обслуживания фрагментов приборами
        # если прибор свободен - то время обслуживания минус бесконечность
        self.list_of_durations_service = [float('-inf') for _ in range(amount_of_devices)]

    # распределяет фрагменты по приборам, устанавливает соответствующее время обслуживания
    def fragments_distribution(self, demand):
        count = 0
        # раскидываем фрагменты по приборам
        for device in self.list_of_devices:
            # если колличесвто свободных приборов больше либо равно количеству фрагментов
            if device.is_free and count < demand.amount_of_fragments:
                # занимаем прибор фрагментом
                device.to_occupy(demand.list_of_fragments[count])
                # записываем длительность обслуживания фрагмента в list_of_durations_service
                self.list_of_durations_service[self.list_of_devices.index(device)] = device.get_service_duration()
                count += 1

    # возвращает количество свободных приборов
    def get_amount_of_free_devices(self):
        amount = 0
        for device in self.list_of_devices:
            # если прибор свободен
            if device.is_free:
                amount += 1
        return amount

    def get_demands_on_devices(self):
        demands_on_devices = []
        for device in self.list_of_devices:
            if not device.is_free() and device.fragment.parent_id not in demands_on_devices:
                demands_on_devices.append(device.fragment.parent_id)
        return demands_on_devices

    # TODO : функцию для поиска ближайшего окончания обслуживания
    #  (т.е минимум из максимумов времени обслуживания требований)

    # возвращает максимальную длительность обслуживания
    def get_max_time(self):
        return max(self.list_of_durations_service)
