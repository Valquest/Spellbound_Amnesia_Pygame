
def enemy_finder(lane_to_search, position_matrix):
    last_position = None
    for lane_index in list(reversed(position_matrix[lane_to_search])):
        if lane_index[2]:
            last_position = lane_index
            break
    return last_position


def damage_enemy(lanes, kill_in_lane, position_matrix, enemy_list, damage=1):
    enemy_to_kill_position = enemy_finder(lanes.index(kill_in_lane), position_matrix)
    for enemy in enemy_list:
        if enemy.position == enemy_to_kill_position:
            enemy.health -= damage


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
