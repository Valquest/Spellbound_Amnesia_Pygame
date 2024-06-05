import pygame
from variables import constants


def add_columns(number_of_cols):
    cols = []
    for spot in range(number_of_cols):
        column = pygame.Rect(constants.COL_START + ((constants.COL_WIDTH - 5) * spot + 1), constants.LANE_START_Y * 3 -
                             constants.MARGIN, constants.COL_WIDTH, constants.WINDOW_HEIGHT - constants.LANE_START_Y *
                             3)
        cols.append(column)
    return cols


def add_lanes(number_of_lanes):
    lanes = []
    for lane_num in range(number_of_lanes):
        lane = pygame.Rect(constants.LANE_START_X, constants.LANE_START_Y * (3 + lane_num) - constants.MARGIN,
                           constants.WINDOW_WIDTH - constants.LANE_START_X - constants.MARGIN, constants.LANE_HEIGHT)
        lanes.append(lane)

    return lanes
