from entities.fragment import Fragment


class Demand:
    """Class describing the essence of a demand consisting of n fragments in a split-merge system."""

    __COUNT = 0

    def __init__(self, arrival_time: float, class_id: int, fragments_number: int) -> None:
        """

        @param arrival_time: time of receipt of the demand in the system
        @param class_id: demand class
        @param fragments_number: the number of fragments that make up the demand
        """
        self.id = Demand.__COUNT
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.leaving_time = None
        self.class_id = class_id
        self.fragments_number = fragments_number
        Fragment.__COUNT = 0
        self.fragments = [Fragment(self.id) for _ in range(fragments_number)]

        Demand.__COUNT += 1

    @staticmethod
    def _reset_counter():
        Demand.__COUNT = 0
