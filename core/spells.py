from core import core_funct


def freeze_enemy(lane, target_enemy_index, turns_frozen, battlefield) -> None:
    lane = battlefield.lanes[lane]
    enemy = lane[target_enemy_index]
    enemy.frozen = turns_frozen


def move_enemy(lane, direction, num_of_spots_moved, battlefield) -> None:
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")

    positions = battlefield.lanes[lane].positions
    num_positions = len(positions)

    # Create a list to store the new states of positions
    new_positions = [None] * num_positions

    # Calculate new positions for all enemies
    for index, position in enumerate(positions):
        if position.occupied and position.card.frozen == 0:
            new_index = index + direction * num_of_spots_moved
            if 0 <= new_index < num_positions:
                new_positions[new_index] = position.enemy
        elif position.card.frozen > 0:
            position.card.frozen -= 1
            new_positions[index] = position.enemy

    # Update the lane with new positions
    for index in range(num_positions):
        if new_positions[index] is not None:
            positions[index].enemy = new_positions[index]
            positions[index].occupied = True
            # Update enemy position coordinates
            positions[index].enemy.update_position(positions[index].rect.centerx, positions[index].rect.centery)
        else:
            positions[index].enemy = None
            positions[index].occupied = False


def damage_enemy(lane_index, battlefield, enemy_list, damage=1, enemy_to_damage: int = 0):
    enemy_to_damage_position = core_funct.enemy_position_finder(lane_index, battlefield, enemy_to_damage)
    for enemy in enemy_list:
        if enemy == enemy_to_damage_position:
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
