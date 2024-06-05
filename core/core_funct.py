import pygame
from variables import constants


def enemy_finder(lane_to_search, position_matrix):
    last_position = None
    for lane_index in list(reversed(position_matrix[lane_to_search])):
        if lane_index[2]:
            last_position = lane_index
            break
    return last_position

def kill_enemy(lanes, kill_in_lane, position_matrix, enemy_list):
    enemy_to_kill_position = enemy_finder(lanes.index(kill_in_lane), position_matrix)
    for enemy in enemy_list:
        if enemy.position == enemy_to_kill_position:
            enemy.health -= 1