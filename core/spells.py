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
        for index, enemy_in_list in enumerate(battlefield.hoard.enemy_list):
            if enemy_in_list == enemy:
                del battlefield.hoard.enemy_list[index]
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


def damage_enemy(lane_index, battlefield, damage=1, enemy_to_damage=None):
    if enemy_to_damage is None:
        enemy_to_damage_index = core_funct.first_last_enemy_finder(battlefield, lane_index, 1)
    else:
        enemy_to_damage_index = enemy_to_damage
    enemy_list = battlefield.hoard.enemy_list
    positions = battlefield.lanes[lane_index].positions
    if enemy_list is not None:
        for enemy in enemy_list:
            if enemy == positions[enemy_to_damage_index].enemy:
                enemy.health -= damage
                if enemy.health <= 0:
                    if enemy.drop is not None:
                        battlefield.hoard.drop_animations.append(enemy)
                    # Remove references to the enemy in the battlefield
                    for lane in battlefield.lanes:
                        for position in lane.positions:
                            if enemy == position.enemy:
                                position.enemy = None

                    # Remove the enemy from the enemy_list
                    enemy_list.remove(enemy)
                    break


def damage_adjacent(lane_index, battlefield, damage=1, target_enemy: int = 0):
    enemy_to_damage_position = core_funct.first_last_enemy_finder(battlefield, lane_index, 1)
    if enemy_to_damage_position is None:
        return
    lanes = battlefield.lanes
    num_of_lanes = len(lanes)
    if lane_index - 1 >= 0:
        if lanes[lane_index - 1].positions[enemy_to_damage_position].enemy is not None:
            damage_enemy(lane_index - 1, battlefield, damage, enemy_to_damage_position)
    if lane_index + 1 < num_of_lanes:
        adjacent_enemy_position = enemy_to_damage_position
        if lanes[lane_index + 1].positions[enemy_to_damage_position].enemy is not None:
            damage_enemy(lane_index + 1, battlefield, damage, enemy_to_damage_position)


def chain_damage(lane_index, battlefield, chain_length, damage=1, target_enemy: int = 0):
    enemy_to_damage_position = core_funct.first_last_enemy_finder(battlefield, lane_index, 1)
    positions = battlefield.lanes[lane_index].positions
    if enemy_to_damage_position is None:
        return
    while enemy_to_damage_position - chain_length < 0:
        chain_length -= 1

    chaining = True
    damage_index = 1
    while chaining:
        if positions[enemy_to_damage_position - damage_index].enemy is not None and chain_length > 0:
            damage_enemy(lane_index, battlefield, damage, enemy_to_damage_position - damage_index)
            damage_index += 1
            chain_length -= 1
        else:
            chaining = False
