from core import core_funct


def freeze_enemy(lane, target_enemy_index, turns_frozen, battlefield) -> None:
    positions = battlefield.lanes[lane].positions
    if target_enemy_index is not None:
        if positions[target_enemy_index] is not None:
            enemy = positions[target_enemy_index].enemy
            enemy.frozen = turns_frozen


def move_enemy(enemy_index, lane, direction, num_of_spots_moved, battlefield) -> None:
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")

    positions = battlefield.lanes[lane].positions
    position_count = len(positions)

    # Check if the specified enemy index is valid
    if not (0 <= enemy_index < len(positions)) or positions[enemy_index].enemy is None:
        raise ValueError("Invalid enemy index")

    enemy = positions[enemy_index].enemy

    # If the enemy is frozen, decrement the frozen counter and do not move
    if enemy.frozen > 0:
        enemy.frozen -= 1
        return

    # Calculate the next position
    next_position = enemy_index + num_of_spots_moved * direction

    # Check if the enemy moves out of bounds
    if next_position >= position_count:
        # Remove the enemy from the battlefield and enemy_list
        for i, e in enumerate(battlefield.lanes[lane].enemy_list):
            if e == enemy:
                del battlefield.lanes[lane].enemy_list[i]
                break
        positions[enemy_index].enemy = None
        return
    elif next_position < 0:
        return  # Do nothing as the enemy cannot move past the start position

    # Check if the next position is not occupied
    if positions[next_position].enemy is None:
        # Move the enemy to the next position
        positions[next_position].enemy = enemy
        positions[enemy_index].enemy = None
        # Update enemy position coordinates
        positions[next_position].enemy.update_position(
            positions[next_position].rect.centerx, positions[next_position].rect.centery
        )


def damage_enemy(lane_index, battlefield, damage=1, enemy_to_damage: int = 0):
    enemy_to_damage_index = core_funct.enemy_position_finder(lane_index, battlefield, enemy_to_damage)
    enemy_list = battlefield.hoard.enemy_list
    positions = battlefield.lanes[lane_index].positions
    if enemy_list is not None:
        for enemy in enemy_list:
            if enemy == positions[enemy_to_damage_index].enemy:
                enemy.health -= damage
                if enemy.health <= 0:
                    # Remove references to the enemy in the battlefield
                    for lane in battlefield.lanes:
                        for position in lane.positions:
                            if enemy == position.enemy:
                                position.enemy = None

                    # Remove the enemy from the enemy_list
                    enemy_list.remove(enemy)
                    break


def damage_adjacent(lane_index, battlefield, damage=1, target_enemy: int = 0):
    enemy_to_damage_position = core_funct.enemy_position_finder(lane_index, battlefield, target_enemy)

    lanes = battlefield.lanes
    num_of_lanes = len(lanes)
    if enemy_to_damage_position is None:
        return

    if lane_index - 1 >= 0:
        if lanes[lane_index - 1].positions[enemy_to_damage_position].enemy is not None:
            damage_enemy(lane_index - 1, battlefield, damage, enemy_to_damage_position)

    if lane_index + 1 < num_of_lanes:
        if lanes[lane_index + 1].positions[enemy_to_damage_position].enemy is not None:
            damage_enemy(lane_index + 1, battlefield, damage, enemy_to_damage_position)
