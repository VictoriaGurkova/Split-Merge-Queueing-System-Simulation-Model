import random

from network_params import Params


class SelectionPolicy:


    @staticmethod
    def direct_order(state: list, params: Params) -> int:
        return 0

    @staticmethod
    def reverse_order(state: list, params: Params) -> int:
        return 1

    @staticmethod
    def random_order(state: list, params: Params) -> int:
        return random.randint(0, 1)

