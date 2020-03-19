from pprint import pprint


class Statistics:
    def __init__(self, list_amounts_of_fragments: list):
        self._amount_of_classes = len(list_amounts_of_fragments)
        self._general_statistics = {
            "amount_of_demands": 0,
            "summary_response_time": 0,
            "average_response_time": 0,
            "summary_time_in_queue": 0,
            "average_time_in_queue": 0
        }
        self._class_statistics = {
            f"class_{i}": self._general_statistics for i in range(self._amount_of_classes)
        }

    def record(self, list_of_demands: list):
        pass

    def show(self):
        pass
