import random
from utils import classes

def last_position_enemy_finder(lane_to_search, position_matrix):
    last_position = None
    for lane_index in list(reversed(position_matrix[lane_to_search])):
        if lane_index[2]:
            last_position = lane_index
            break
    return last_position


def damage_enemy(lane_index, position_matrix, enemy_list, damage=1):
    enemy_to_damage_position = last_position_enemy_finder(lane_index, position_matrix)
    for enemy in enemy_list:
        if enemy.position == enemy_to_damage_position:
            enemy.health -= damage


def generate_enemies(enemy_list, buffer_int, enemy_matrix):
    for _ in range(buffer_int):
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        random_row = random.randint(0, len(enemy_matrix) - 1)

        for index, col in enumerate(enemy_matrix[random_row]):
            if not col[2]:
                enemy = classes.Enemy(enemy_matrix[random_row][index][1],
                                      enemy_matrix[random_row][index][0],
                                      random_color)
                enemy_matrix[random_row][index][2] = True
                enemy.position = enemy_matrix[random_row][index]
                enemy.health = random.randint(1, 3)
                enemy_list.append(enemy)
                break


def calculate_return_path(start_pos, end_pos, steps=20):
    path = []
    for step in range(steps):
        t = step / (steps - 1)
        # calculate curved path using a quadratic Bezier curve
        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = min(start_pos[1], end_pos[1]) - 50
        x = (1 - t)**2 * start_pos[0] + 2 * (1 - t) * t * mid_x + t**2 * end_pos[0]
        y = (1 - t)**2 * start_pos[1] + 2 * (1 - t) * t * mid_y + t**2 * end_pos[1]
        path.append((x, y))
    return path


# finds enemy position index inside a lane list based of an enemy instance of Enemy class
def enemy_position_index_finder(enemy, lane_list):
    enemy_pos = enemy.position
    current_index = None
    for i, pos in enumerate(lane_list):
        if pos[:2] == enemy_pos[:2]:
            current_index = i
            break

    # current_index = next((i for i, pos in enumerate(lane_matrix) if pos[:2] == enemy_pos[:2]), None)

    return current_index


def enemy_list_sorter(enemy_list):
    return sorted(enemy_list, key=lambda enemy: (enemy.position[1], enemy.position[0]))


def move_enemy(lane, direction, num_of_spots_moved, enemy_list, map_matrix):
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")
    else:
        lane_list = map_matrix[lane]
        num_positions = len(lane_list)
        # sort enemy list
        enemy_list = enemy_list_sorter(enemy_list)
        # based on direction we set lane_list order, so we could move enemies only if they are not colliding with other
        # enemies
        if direction == 1:
            lane_list = list(reversed(map_matrix[lane]))
        elif direction == -1:
            lane_list = list(reversed(map_matrix[lane]))

        # after lists are established we find position indexes for enemies, set new indexes and check if new indexes
        # are valid
        for enemy in enemy_list:
            current_index = enemy_position_index_finder(enemy, lane_list)
            if current_index is not None:
                for moves in range(num_of_spots_moved, 0, -1):
                    new_index = current_index - direction * moves
                    if 0 <= new_index < num_positions and not lane_list[new_index][2]:
                        # store move queue information in order to complete movements in the right order
                        lane_list[current_index][2] = False
                        lane_list[new_index][2] = True
                        enemy.position = lane_list[new_index]
                        enemy.update_position()

    return enemy_list
