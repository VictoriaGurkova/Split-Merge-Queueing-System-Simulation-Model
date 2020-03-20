from Device import Device


# класс-обертка для приборов
# содержит некоторые вспомогательные методы
class Wrapper_for_Devices:
    def __init__(self, mu, amount_of_devices):
        self.mu = mu
        # генерируется список amount_of_devices приборов с интенсивностями mu
        self.list_of_devices = [Device(self.mu) for _ in range(amount_of_devices)]

    # распределяет фрагменты по приборам, устанавливает соответствующее время обслуживания
    def distribute_fragments(self, demand, current_time):
        count = 0
        # раскидываем фрагменты по приборам
        for device in self.list_of_devices:
            # если колличесвто свободных приборов больше либо равно количеству фрагментов
            if device.is_free and count < demand.amount_of_fragments:
                # занимаем прибор фрагментом
                device.to_occupy(demand.list_of_fragments[count], current_time)
                count += 1

    # возвращает количество свободных приборов
    def get_amount_of_free_devices(self):
        return len([True for device in self.list_of_devices if device.is_free])

    # возвращает ближайшее время окончания обслуживания требования
    def get_min_end_service_time_for_demand(self):
        lists_of_service_duration_fragments = self.get_lists_of_service_duration_fragments()
        # список длительностей обслуживания всех требований на приборах в данный момент
        max_service_duration_of_fragments = []
        for duration in lists_of_service_duration_fragments:
            max_service_duration_of_fragments.append(max(duration))
        return min(max_service_duration_of_fragments)

    # возвращает список списков длительностей обслуживания фрагментов каждого требования в сети
    def get_lists_of_service_duration_fragments(self):
        list_demands_on_devices = self.get_id_demands_on_devices()
        lists_of_service_duration_fragments = [[] for _ in range(len(list_demands_on_devices))]
        # проходим по списку id требований, которые сейчас находятся на обслуживании
        for id_demand in list_demands_on_devices:
            # проходим по всем приборам
            for device in self.list_of_devices:
                # если фрагмент на данном приборе принадлежит требованию с id равным id_demand
                if not device.is_free and device.fragment.parent_id == id_demand:
                    # заполняем список длительностями обслуживания фрагментов данного требования
                    lists_of_service_duration_fragments[list_demands_on_devices.index(id_demand)] \
                        .append(device.service_duration)
        return lists_of_service_duration_fragments

    def get_id_demands_on_devices(self):
        id_demands_on_devices = set()
        for device in self.list_of_devices:
            if not device.is_free:
                id_demands_on_devices.add(device.fragment.parent_id)
        return list(id_demands_on_devices)

    def get_id_demand_with_min_end_service_time(self):
        for device in self.list_of_devices:
            if device.service_duration == self.get_min_end_service_time_for_demand():
                return device.fragment.parent_id

    def to_free_demand_fragments(self, demand_id):
        for device in self.list_of_devices:
            if not device.is_free and device.fragment.parent_id == demand_id:
                device.to_free()
