from variables import constants, variables
from classes import battle_classes


def add_amnesia_bar(number_of_amnesia_steps: int) -> list:
    """
    Generates rect objects for amnesia bar, to track when wizard will fail to select the right card
    :param number_of_amnesia_steps: A number of steps in an amnesia meter
    :return: a list of rect objects
    """
    meter = []
    for step in range(number_of_amnesia_steps):
        starting_x = variables.amnesia_bar_x + (2 * battle_classes.Meter.width) * step
        meter_box = battle_classes.Meter(starting_x, True)
        meter.append(meter_box)
    return meter


def increment_amnesia_bar(meter_list: list):
    """
    Updates the infill of amnesia bar rect objects
    :param meter_list: A list of meter class objects
    :return:
    """
    final_meter = constants.AMNESIA_BAR_COUNT - 1
    if not meter_list[final_meter].border:
        for meter in meter_list:
            meter.border = True
    else:
        for meter in meter_list:
            if meter.border:
                meter.border = False
                break
