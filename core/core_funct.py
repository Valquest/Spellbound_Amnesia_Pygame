import random
from classes import battle_classes
from variables import constants
from data import entities


def first_last_enemy_finder(battlefield, lane_to_search, first_or_last) -> int or None:
    """
    :param battlefield:
    :param lane_to_search:
    :param first_or_last: -1 - finds last enemy, 1 - finds first enemy
    :return: an integer value of an enemy index or None
    """
    lane = battlefield.lanes[lane_to_search]
    enemy_list = [position.enemy for position in lane.positions if position.enemy is not None]
    enemy_position = None
    target_enemy = None
    if enemy_list:
        if first_or_last == 1:
            target_enemy = list(reversed(enemy_list))[0]
        elif first_or_last == -1:
            target_enemy = enemy_list[0]
        for index, position in enumerate(lane.positions):
            if position.enemy == target_enemy:
                enemy_position = index
    return enemy_position


def enemy_position_finder(lane_to_search, battlefield, enemy_to_look_for: int = 0, next_to: bool = False) -> int or None:
    """
    Functions locates requested enemy index position inside its lane
    :param lane_to_search: lane index number
    :param battlefield: a multi level class that stores lane and position class elements
    :param enemy_to_look_for: integer number of index for which enemy to find
    :param next_to: if looking for subsequent enemy, find only ones next to previous
    :return: returns the position index of the enemy
    """
    lanes = battlefield.lanes
    lane = lanes[lane_to_search]
    reversed_positions_list = list(reversed(lane.positions))
    enemy_position_index_list = [index for index, position in enumerate(reversed_positions_list) if position.enemy]

    if not enemy_position_index_list:  # No enemies found
        return None

    if enemy_to_look_for == 0 or enemy_to_look_for >= len(enemy_position_index_list):
        return enemy_position_index_list[0]

    if next_to and enemy_to_look_for > 0:
        if enemy_position_index_list[enemy_to_look_for] - 1 == enemy_position_index_list[enemy_to_look_for - 1]:
            return enemy_position_index_list[enemy_to_look_for]
        return None

    return enemy_position_index_list[enemy_to_look_for]


def calculate_return_path(start_pos, end_pos, steps=20) -> list:
    """
    Calculates a return path for a card that was just hovering over a lane and needs to return back to original position.
    :param start_pos: Cards start position as a list containing x and y positions.
    :param end_pos: Cards current position as a list containing x and y positions.
    :param steps: Number of steps card needs to take to return back.
    :return: A list of positions card needs to appear in to smoothly return back.
    """
    path = []
    for step in range(steps):
        # ensures that t varies linearly from 0 to 1 over the number of steps
        t = step / (steps - 1)
        # calculate curved path using a quadratic Bezier curve
        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = min(start_pos[1], end_pos[1]) - 50
        x = (1 - t)**2 * start_pos[0] + 2 * (1 - t) * t * mid_x + t**2 * end_pos[0]
        y = (1 - t)**2 * start_pos[1] + 2 * (1 - t) * t * mid_y + t**2 * end_pos[1]
        path.append((x, y))

    return path


def enemy_list_sorter(enemy_list) -> list:
    """
    Sorts enemy list, so they are arranged in order that each position for for row 1 is arranged first, followed by lane 2
    and lane 3
    :param enemy_list:
    :return: a sorted enemy list
    """
    # return a new list sorted in a priority order y and then x coordinates
    return sorted(enemy_list, key=lambda enemy: (enemy.y_cord, enemy.x_cord))


# generating game cards
def create_card_list() -> list:
    """
    Generates a list of Card class objects, each Card object has a rect object and few functions to manage these objects
    :return: returns a list of Card class objects
    """
    game_cards = []
    for count in range(constants.CARD_COUNT):
        random_item = random.choice(list(entities.card_types.items()))
        card = battle_classes.Card(150 * count + 1, 0, "gray")

        # take random card type and damage value from the card type dictionary
        card.type = random_item[0]
        card.params = random_item[1]
        card.position = [150 * count + 1 + constants.MARGIN, 0 + constants.MARGIN]

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
            # take random card type and parameter value from the card type dictionary
            random_item = random.choice(list(entities.card_types.items()))
            cards[card_index].type = random_item[0]
            cards[card_index].params = random_item[1]

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
