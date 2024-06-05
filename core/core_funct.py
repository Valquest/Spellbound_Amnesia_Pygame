import pygame
from variables import constants


def enemy_finder(lane_to_search, matrix):
    last_position = None
    for lane_index in list(reversed(matrix[lane_to_search])):
        if lane_index[2]:
            last_position = lane_index
            break
    return last_position
