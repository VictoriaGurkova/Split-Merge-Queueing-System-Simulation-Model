from random import random

from network_params import Params


def define_arriving_demand_class(prob: float):
    return 0 if random() < prob else 1


def set_events_times(times: dict, config: dict, params: Params):
    if config["devices"].check_if_possible_put_demand_on_devices(params):
        times["service_start"] = times["current"]
    if not config["devices"].get_id_demands_on_devices():
        times["leaving"] = float('inf')
    else:
        times["leaving"] = config["devices"].get_min_end_service_time_for_demand()
