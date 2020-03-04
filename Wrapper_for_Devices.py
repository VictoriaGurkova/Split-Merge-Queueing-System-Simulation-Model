from Device import Device


# класс-обертка для приборов
# содержит некоторые вспомогательные методы
class Wrapper_for_Devices:
    def __init__(self, mu, amount_of_devices):
        self.mu = mu
        # генерируется список amount_of_devices приборов с интенсивностями mu
        self.list_of_devices = [Device(self.mu) for _ in range(amount_of_devices)]

    # распределяет фрагменты по приборам, устанавливает соответствующее время обслуживания
    def fragments_distribution(self, demand):
        count = 0
        # раскидываем фрагменты по приборам
        for device in self.list_of_devices:
            # если колличесвто свободных приборов больше либо равно количеству фрагментов
            if device.is_free and count < demand.amount_of_fragments - 1:
                # занимаем прибор фрагментом
                device.to_occupy(demand.list_of_fragments[count])
                count += 1

    # возвращает количество свободных приборов
    def get_amount_of_free_devices(self):
        amount = 0
        for device in self.list_of_devices:
            # если прибор свободен
            if device.is_free:
                amount += 1
        return amount

    def get_min_service_duration_for_demand(self):

        for id_demand in self.get_demands_on_devices():
            for device in self.list_of_devices:
                if not device.is_free() and device.fragment.parent_id == id_demand:
                    # TODO: определить ближайшее завершение обслуживание требования
                    pass

    def get_demands_on_devices(self):
        id_demands_on_devices = []
        for device in self.list_of_devices:
            if not device.is_free() and device.fragment.parent_id not in id_demands_on_devices:
                id_demands_on_devices.append(device.fragment.parent_id)
        return id_demands_on_devices

    # TODO : функцию для поиска ближайшего окончания обслуживания
    #  (т.е минимум из максимумов времени обслуживания требований)
