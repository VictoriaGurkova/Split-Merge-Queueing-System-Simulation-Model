from random import random

from network_params import Params


def define_arriving_demand_class(prob: float):
    return 0 if random() < prob else 1


def set_events_times(times: dict, config: dict, params: Params):
    if check_if_possible_put_demand_on_devices(config, params):
        times["service_start"] = times["current"]
    if not config["devices"].get_id_demands_on_devices():
        times["leaving"] = float('inf')
    else:
        times["leaving"] = config["devices"].get_min_end_service_time_for_demand()


# TODO: replace in wrapper
def can_occupy(class_id: int, config: dict, params: Params):
    """Checking whether the demand of this class can take place on the devices

    # TODO: write descriptions
    :param params:
    :param config:
    :param class_id: demand class
    """

    return config["devices"].get_amount_of_free_devices() >= params.fragments_amounts[class_id]


def check_if_possible_put_demand_on_devices(config: dict, params: Params):
    """Checking whether it is possible to place a demand on devices"""

    return len([True for class_id in range(len(params.fragments_amounts))
                if can_occupy(class_id, config, params)])
