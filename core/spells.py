from core import core_funct


def freeze_enemy(lane, target_enemy_index, turns_frozen, battlefield) -> None:
    positions = battlefield.lanes[lane].positions
    if target_enemy_index is not None:
        if positions[target_enemy_index] is not None:
            enemy = positions[target_enemy_index].enemy
            enemy.frozen = turns_frozen


# def move_enemy(lane, direction, num_of_spots_moved, battlefield, enemy_list, enemy_to_move=None) -> None or int:
#     if direction not in [-1, 1]:
#         raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")
#
#     positions = battlefield.lanes[lane].positions
#     position_count = len(positions)
#     enemy_index_list = list(reversed([index for index, position in enumerate(positions) if position.enemy is not None]))
#     health_lost = False
#
#     enemies = [enemy for enemy in positions if enemy.enemy is not None]
#     for enemy in enemies:
#         print(f"Enemy: {positions.index(enemy)}, frozen status: {enemy.frozen}")
#
#     # if specific enemy has to be moved we set up a target enemy
#     target_enemy = None
#     if enemy_to_move is not None:
#         for enemy in enemy_index_list:
#             if positions[enemy].enemy == positions[enemy_to_move].enemy:
#                 target_enemy = enemy
#
#     # if list is empty, no enemies need to move
#     if not enemy_index_list:
#         return
#
#     if target_enemy is not None:
#         if 1 <= target_enemy < len(positions):
#             if positions[target_enemy].enemy.frozen == 0:
#                 next_position = target_enemy + num_of_spots_moved * direction
#                 positions[next_position].enemy = positions[target_enemy].enemy
#                 positions[target_enemy].enemy = None
#                 # Update enemy position coordinates
#                 positions[next_position].enemy.update_position(
#                     positions[next_position].rect.centerx, positions[next_position].rect.centery)
#
#     else:
#         for index in enemy_index_list:
#             print(f"for enemy index {index}")
#             next_index = index + num_of_spots_moved * direction
#             if next_index >= position_count and positions[index].enemy.frozen == 0:
#                 # return 1 if enemy has moved past last position and player should lose health
#                 for enemy in enemy_list:
#                     if enemy == positions[index].enemy:
#                         enemy_list.remove(enemy)
#                         break
#                 positions[index].enemy = None
#                 enemy_index_list = list(
#                     reversed([index for index, position in enumerate(positions) if position.enemy is not None]))
#                 print(f"After removing first enemy: {enemy_index_list}")
#                 health_lost = True
#             # 2 following ifs check if future position is not occupied, not out of lane and enemy is not frozen
#             elif 0 < next_index < position_count:
#                 print(f"Pre checking if enemy exists in next index {enemy_index_list}")
#                 print({positions[next_index].enemy is None and positions[index].enemy.frozen == 0})
#                 if positions[next_index].enemy is None and positions[index].enemy.frozen == 0:
#                     positions[next_index].enemy = positions[index].enemy
#                     positions[index].enemy = None
#                     # Update enemy position coordinates
#                     positions[next_index].enemy.update_position(
#                         positions[next_index].rect.centerx, positions[next_index].rect.centery)
#                     enemy_index_list = list(
#                         reversed([index for index, position in enumerate(positions) if position.enemy is not None]))
#                     print(f"Post list changes: {enemy_index_list}")
#                     print("-------")
#                 elif positions[index].enemy.frozen > 0:
#                     positions[index].enemy.frozen -= 1
#     return health_lost


def move_enemy(enemy_index, lane, direction, num_of_spots_moved, battlefield, enemy_list) -> None or int:
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
        for i, e in enumerate(enemy_list):
            if e == enemy:
                del enemy_list[i]
                break
        positions[enemy_index].enemy = None
        return 1  # Indicating health lost as enemy moved past the last position
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

    return None


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
