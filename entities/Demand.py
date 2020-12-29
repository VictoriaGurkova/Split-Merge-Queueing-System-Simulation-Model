from entities.Fragment import Fragment


class Demand:
    """Class describing the essence of a demand consisting of n fragments in a split-merge system."""

    __COUNT = 0

    def __init__(self, arrival_time: float, class_id: int, amount_of_fragments: int):
        """

        :param arrival_time: time of receipt of the demand in the system
        :param class_id: demand class
        :param amount_of_fragments: the number of fragments that make up the demand
        """
        Demand.__COUNT += 1
        self.id = Demand.__COUNT
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.leaving_time = None
        self.class_id = class_id
        self.amount_of_fragments = amount_of_fragments
        Fragment.__COUNT = 0
        self.fragments = [Fragment(self.id) for _ in range(amount_of_fragments)]
