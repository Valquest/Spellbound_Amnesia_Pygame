from core import core_funct


def freeze_enemy(lane, target_enemy_index, turns_frozen, battlefield) -> None:
    positions = battlefield.lanes[lane].positions
    if target_enemy_index is not None:
        if positions[target_enemy_index] is not None:
            enemy = positions[target_enemy_index].enemy
            enemy.frozen = turns_frozen


def move_enemy(lane, direction, num_of_spots_moved, battlefield, enemies_to_move=None) -> None or int:
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")
    positions = battlefield.lanes[lane].positions
    position_count = len(positions)
    enemy_index_list = list(reversed([index for index, position in enumerate(positions) if position.enemy is not None]))

    # if list is empty, no enemies need to move
    if not enemy_index_list:
        return

    for index in enemy_index_list:
        next_index = index + num_of_spots_moved * direction
        # 2 following ifs check if future position is not occupied, not out of lane and enemy is not frozen
        if 0 < next_index < position_count:
            if positions[next_index].enemy is None and positions[index].enemy.frozen == 0:
                positions[next_index].enemy = positions[index].enemy
                positions[index].enemy = None
                # Update enemy position coordinates
                positions[next_index].enemy.update_position(
                    positions[next_index].rect.centerx, positions[next_index].rect.centery)
                enemy_index_list = list(
                    reversed([index for index, position in enumerate(positions) if position.enemy is not None]))
            elif positions[index].enemy.frozen > 0:
                positions[index].enemy.frozen -= 1
        elif next_index >= position_count and positions[index].enemy.frozen == 0:
            # return 1 if enemy has moved past last position and player should lose health
            return 1



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
