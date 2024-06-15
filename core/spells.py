from core import core_funct


def freeze_enemy(lane, target_enemy_index, turns_frozen, battlefield) -> None:
    positions = battlefield.lanes[lane].positions
    if positions[target_enemy_index] is not None:
        enemy = positions[target_enemy_index].enemy
        enemy.frozen = turns_frozen


def move_enemy(lane, direction, num_of_spots_moved, battlefield, enemies_to_move=None) -> None:
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")
    positions = battlefield.lanes[lane].positions
    num_positions = len(positions)

    # Create a list to store the new states of positions
    new_positions = [None] * num_positions

    # Calculate new positions for specified enemies or all if not specified
    for index, position in enumerate(positions):
        if position.enemy is not None:
            # Check if the enemy is frozen
            if position.enemy.frozen > 0:
                position.enemy.frozen -= 1
                new_positions[index] = position.enemy  # Assign enemy back to the same position
                continue  # Skip to the next iteration, preventing any further logic from moving this enemy

            # Move non-frozen enemies if no specific enemies are designated or index is in designated list
            if position.enemy.frozen == 0 and (enemies_to_move is None or index in enemies_to_move):
                new_index = index + direction * num_of_spots_moved
                if 0 <= new_index < num_positions:
                    new_positions[new_index] = position.enemy

    # Update the lane with new positions
    for index in range(num_positions):
        if new_positions[index] is not None:
            positions[index].enemy = new_positions[index]
            # Update enemy position coordinates
            positions[index].enemy.update_position(positions[index].rect.centerx, positions[index].rect.centery)
        else:
            positions[index].enemy = None


def damage_enemy(lane_index, battlefield, enemy_list, damage=1, enemy_to_damage: int = 0):
    enemy_to_damage_position = core_funct.enemy_position_finder(lane_index, battlefield, enemy_to_damage)
    if enemy_list is not None:
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
