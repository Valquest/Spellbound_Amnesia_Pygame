import random
from utils import classes
from variables import constants
from data import entities


def enemy_position_finder(lane_to_search, battlefield, enemy_to_look_for: int = 0, next_to: bool = False) -> list:
    """
    Functions locates requested enemy index position inside its lane
    :param lane_to_search: lane index number
    :param battlefield: a multi level class that stores lane and position class elements
    :param enemy_to_look_for: integer number of index for which enemy to find
    :param next_to: if looking for subsequent enemy, find only ones next to previous
    :return: returns a list with position information (x, y, bool)
    """
    lanes = battlefield.lanes
    reversed_list = list(reversed(lanes[lane_to_search].positions))
    enemy_position_list = [index for index, position in enumerate(reversed_list) if position.occupied]
    last_position = None
    # checks if requested enemy is within the list or is not the first enemy in the list
    if 0 < enemy_to_look_for < len(reversed_list):
        if next_to:
            # checks if enemy, being looked, for has index that is 1 more than previous enemy (subsequent)
            if enemy_position_list[enemy_to_look_for] - 1 == enemy_position_list[enemy_to_look_for - 1]:
                last_position = enemy_position_list[enemy_to_look_for]
            else:
                last_position = None
        else:
            last_position = enemy_position_list[enemy_to_look_for]
    else:
        last_position = enemy_position_list[0]

    return reversed_list[last_position]


def damage_enemy(lane_index, battlefield, enemy_list, damage=1, enemy_to_damage: int = 0):
    enemy_to_damage_position = enemy_position_finder(lane_index, battlefield, enemy_to_damage)
    for enemy in enemy_list:
        print(enemy.position)
        if enemy.position == enemy_to_damage_position:
            enemy.health -= damage


# def generate_enemies(enemy_list, buffer_int, enemy_matrix):
#     for _ in range(buffer_int):
#         random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         random_row = random.randint(0, len(enemy_matrix) - 1)
#
#         for index, col in enumerate(enemy_matrix[random_row]):
#             if not col[2]:
#                 enemy = classes.Enemy(enemy_matrix[random_row][index][1],
#                                       enemy_matrix[random_row][index][0],
#                                       random_color)
#                 enemy_matrix[random_row][index][2] = True
#                 enemy.position = enemy_matrix[random_row][index]
#                 enemy.health = random.randint(1, 3)
#                 enemy_list.append(enemy)
#                 break


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
# def enemy_position_index_finder(enemy, lane_list):
#     enemy_pos = enemy.position
#     current_index = None
#     for i, pos in enumerate(lane_list):
#         if pos[:2] == enemy_pos[:2]:
#             current_index = i
#             break
#
#     # current_index = next((i for i, pos in enumerate(lane_matrix) if pos[:2] == enemy_pos[:2]), None)
#
#     return current_index


def enemy_list_sorter(enemy_list):
    # return a new list sorted in a priority order y and then x coordinates
    return sorted(enemy_list, key=lambda enemy: (enemy.y_cord, enemy.x_cord))


def move_enemy(lane, direction, num_of_spots_moved, battlefield) -> None:
    if direction not in [-1, 1]:
        raise ValueError("Direction must be either 1 or -1 for \"move_enemy\" function")
    else:
        positions = battlefield.lanes[lane].positions
        num_positions = len(positions)
        # sort enemy list
        #           enemy_list = enemy_list_sorter(enemy_list)
        # based on direction we set lane_list order, so we could move enemies only if they are not colliding with other
        # enemies
        lane_list = list(reversed(positions))

        # after lists are established we find position indexes for enemies, set new indexes and check if new indexes
        # are valid
        for index, position in enumerate(positions):
            for moves in range(num_of_spots_moved, 0, -1):
                new_index = index - direction * moves
                if 0 <= new_index < num_positions and not lane_list[new_index].occupied:
                    # store move queue information in order to complete movements in the right order
                    lane_list[index].occupied = False
                    lane_list[new_index].enemy = lane_list[index].enemy
                    lane_list[index].enemy = None
                    lane_list[new_index].occupied = True


# generating game cards
def create_card_list() -> list:
    """
    Generates a list of Card class objects, each Card object has a rect object and few functions to manage these objects
    :return: returns a list of Card class objects
    """
    game_cards = []
    for count in range(constants.CARD_COUNT):
        random_item = random.choice(list(entities.card_types.items()))
        card = classes.Card(150 * count + 1, 0, "gray")

        # take random card type and damage value from the card type dictionary
        card.type = random_item[0]
        card.damage = random_item[1][0]
        card.position = [150 * count + 1 + constants.MARGIN, 0 + constants.MARGIN]
        card.enemy_to_damage = random_item[1][1]

        game_cards.append(card)
    return game_cards


def modify_card_list(card_list: list, cards_to_modify: list[int] = None):
    """
    Modifies a list of cards to get a random card type and a damage value associated to that card type.
    :param card_list: - A list of Card class objects
    :param cards_to_modify: - A list of index numbers targeting items that need to be modified in the card_list list. If
    no value is provided, all cards will be updated
    :return:
    """
    def modify(cards: list, to_modify: list):
        for card_index in to_modify:
            random_item = random.choice(list(entities.card_types.items()))
            cards[card_index].type = random_item[0]
            cards[card_index].damage = random_item[1][0]

    if cards_to_modify is None:
        cards_to_modify = [i - 1 for i in range(constants.CARD_COUNT)]
        modify(card_list, cards_to_modify)

    elif len(cards_to_modify) == 1 and cards_to_modify[0] + 1 == constants.CARD_COUNT:
        modify(card_list, cards_to_modify)

    else:
        for index in cards_to_modify:
            for i in range(index, len(card_list) - 1):
                card_list[i].position, card_list[i + 1].position = card_list[i + 1].position, card_list[i].position
            modify(card_list, [index])
