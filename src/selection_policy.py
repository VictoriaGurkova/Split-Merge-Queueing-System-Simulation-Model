from network_params import Params


class SelectionPolicy:

    @staticmethod
    def choice(state: list, params: Params):
        pass

    @staticmethod
    def direct_order(state: list, params: Params) -> int:
        return 0

    @staticmethod
    def reverse_order(state: list, params: Params) -> int:
        return 1
