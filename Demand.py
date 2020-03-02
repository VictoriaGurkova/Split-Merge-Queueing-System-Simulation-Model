from Fragment import Fragment


class Demand:
    count = 0

    def __init__(self, arrival_time, amount_of_fragments):
        Demand.count += 1
        self.id = Demand.count
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.leaving_time = None
        self.amount_of_fragments = amount_of_fragments
        Fragment.count = 0
        self.list_of_fragments = [Fragment(self.id) for _ in range(amount_of_fragments)]
