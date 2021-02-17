import logging

logging.basicConfig(filename="logging.log", level=logging.ERROR, filemode="w")


def log_arrival(demand, current_time):
    logging.debug("Demand arrival: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                  ". Current Time: " + str(current_time))


def log_full_queue(demand, current_time):
    logging.debug(
        "Demand arrival (FULL QUEUE): ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
        ". Current Time: " + str(current_time))


def log_service_start(demand, current_time):
    logging.debug("Demand start service: ID - " + str(demand.id) + ". Class ID - " +
                  str(demand.class_id) + ". Current Time: " + str(current_time))


def log_leaving(demand, current_time):
    logging.debug("Demand leaving: ID - " + str(demand.id) + ". Class ID - " + str(demand.class_id) +
                  ". Current Time: " + str(current_time))


def log_network_state(times, devices):
    logging.debug("Device's state: " + str(devices.get_id_demands_on_devices()))
    logging.debug("Device's state with min time: " +
                  str(devices.get_service_duration_fragments()))
    logging.debug("Event times: = " +
                  str([times.arrival, times.service_start, times.leaving]))
