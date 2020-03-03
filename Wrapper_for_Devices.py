from Device import Device


class Wrapper_for_Devices:
    def __init__(self, mu, amount_of_devices):
        self.mu = mu
        # генерируется список amount_of_devices приборов с интенсивностями mu
        self.list_of_devices = [Device(self.mu) for _ in range(amount_of_devices)]
        # список для хранения длительностей обслуживания фрагментов приборами
        self.list_of_durations_service = [float('-inf') for _ in range(amount_of_devices)]

    def fragments_distribution(self, demand):
        count = 0
        for device in self.list_of_devices:
            if device.is_free and count < demand.amount_of_fragments:
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
