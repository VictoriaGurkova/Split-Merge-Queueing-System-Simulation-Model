from network_params import Params


class SelectionPolicy:

    @staticmethod
    def choice(state: list, params: Params):
        pass

    @staticmethod
    def always_from_first(state: list, params: Params) -> int:
        return 0

    @staticmethod
    def always_from_second(state: list, params: Params) -> int:
        return 1

    @staticmethod
    def direct_order(state: list, params: Params) -> int:
        if state[0]:
            return 0
        else:
            return 1

    @staticmethod
    def reverse_order(state: list, params: Params) -> int:
        if state[1]:
            return 1
        else:
            return 0

    @staticmethod
    def new_selection_policy(state: list, params: Params):
        pass
