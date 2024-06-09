import pygame
import random
# project files
from utils import classes
from variables import constants, variables
from core import core_funct
from utils import util_funct


def main():

    # pygame setup
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    pygame.display.set_caption('Spellbound Amnesia')

    # creating enemy position matrix for coordinates and slot availability. This is used to determine what positions in
    # the field are available and will be used for combat to determine what effects apply to what lanes
    enemy_position_matrix = []
    for row in range(constants.ROW_NUMBER):
        row_position = []
        for col in range(constants.COL_NUMBER):
            x_pos = int(round((constants.WINDOW_WIDTH -
                               constants.MARGIN - ((variables.col_width - constants.BORDER_THICKNESS) * col) -
                               variables.col_width / 2), 0))
            y_pos = int(round((constants.WINDOW_HEIGHT -
                               constants.MARGIN - (variables.lane_height * (3 - row))
                               + variables.lane_height / 2), 0))
            occupied = False
            position = [x_pos, y_pos, occupied]
            row_position.append(position)
        enemy_position_matrix.append(row_position)

    # create amnesia meter bar
    meter = util_funct.add_amnesia_bar(constants.AMNESIA_BAR_COUNT)

    # create lanes/rows
    lanes = util_funct.add_lanes(constants.ROW_NUMBER)

    # create spots/columns
    spots = util_funct.add_columns(constants.COL_NUMBER)

    # generating game cards
    cards = core_funct.create_card_list()

    # generate enemies
    enemies = []
    number_of_enemies = random.randint(4, 8)
    core_funct.generate_enemies(enemies, number_of_enemies, enemy_position_matrix)
    # for _ in range(random.randint(4, 8)):
    #     random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #     random_row = random.randint(0, len(enemy_position_matrix) - 1)
    #
    #     for index, col in enumerate(enemy_position_matrix[random_row]):
    #         if not col[2]:
    #             enemy = classes.Enemy(enemy_position_matrix[random_row][index][1],
    #                                   enemy_position_matrix[random_row][index][0],
    #                                   random_color)
    #             enemy_position_matrix[random_row][index][2] = True
    #             enemy.position = enemy_position_matrix[random_row][index]
    #             enemy.health = random.randint(1, 3)
    #             enemies.append(enemy)
    #             break

    # generate a start turn button and text
    start_turn_btn = pygame.Rect((classes.Card.card_width + constants.MARGIN) * constants.CARD_COUNT + 100,
                                 constants.MARGIN, 200, 50)

    turn_ended = False
    end_btn_font = pygame.font.Font(None, 32)
    render_btn_font = end_btn_font.render("Start Turn", True, (0, 0, 0))
    start_turn_btn_position = render_btn_font.get_rect(center=((cards[0].card_width + constants.MARGIN) *
                                                               constants.CARD_COUNT + 100 + 200 // 2,
                                                               constants.MARGIN + 50 // 2))

    # this code draws all enemies in all possible positions to test if positioning is correct
    # for row in range(constants.ROW_NUMBER):
    #     for col in range(constants.COL_NUMBER):
    #         random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #         enemy = Enemy(enemy_position_matrix[row][col][1] - Enemy.enemy_width / 2,
    #                       enemy_position_matrix[row][col][0] - Enemy.enemy_height / 2, random_color)
    #         enemies.append(enemy)

    # MAIN GAME LOOP

    # game loop variables
    selected_lane = None
    selected_card = None
    move_selections = []

    # turn related variables
    total_actions = 3
    current_action = 1
    action_start_time = 0
    delay_between_actions = 100

    # card movement variables
    returning_card = None
    card_offset_x = 0
    card_offset_y = 0
    returning_path = []
    card_animation_index = 0

    while running:
        # poll for events
        # pygame.Quit event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                mouse_pos = pygame.mouse.get_pos()
                """
                # check if clicked inside any rectangle and damage enemies
                for lane in lanes:
                    if lane.collidepoint(mouse_pos):
                        selected_lane = lanes.index(lane)

                        # damage enemy when lane is selected
                        #core_funct.damage_enemy(lanes.index(lane), enemy_position_matrix, enemies, 1)

                        # exits loop if condition is met
                        break
                """
                if start_turn_btn.collidepoint(mouse_pos):
                    turn_ended = True
                    action_start_time = pygame.time.get_ticks()

                for card in cards:
                    if pygame.Rect(card.x_cord, card.y_cord, card.card_width, card.card_height).collidepoint(event.pos):
                        selected_card = card
                        card_offset_x = card.x_cord - event.pos[0]
                        card_offset_y = card.y_cord - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_card:
                    for lane in lanes:
                        if lane.collidepoint(pygame.mouse.get_pos()):
                            lane_index = lanes.index(lane)
                            move_index = -1
                            print(f"Card {cards.index(selected_card)} touched Lane {lane_index}")
                            for index, selection in enumerate(move_selections):
                                if selection[0] == selected_card:
                                    move_index = index
                                    break

                            if move_index != -1:
                                move_selections[move_index][1] = lane_index
                                # noinspection PyUnusedLocal
                                move_index = -1
                            elif len(move_selections) < 3:
                                move_selections.append([selected_card, lane_index])
                            else:
                                move_selections.pop(0)
                                move_selections.append([selected_card, lane_index])

                            break

                    # Calculate returning path
                    returning_path = core_funct.calculate_return_path(
                        (selected_card.x_cord, selected_card.y_cord),
                        (selected_card.original_x, selected_card.original_y))
                    returning_card = selected_card
                    card_animation_index = 0
                    selected_card = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_card:
                    selected_card.update_position(event.pos[0] + card_offset_x, event.pos[1] + card_offset_y)

        current_time = pygame.time.get_ticks()

        # turn based action logic, every action takes 2 seconds to complete, 3 seconds delay between turns
        if turn_ended:
            if current_action <= total_actions * 3:  # Ensure to perform all actions 3 times
                if current_time - action_start_time > delay_between_actions:
                    sequence_index = (current_action - 1) % 3  # Cycle through 0, 1, 2

                    if sequence_index == 0:
                        # damaging enemies
                        if (current_action - 1) // 3 < len(move_selections):
                            action = move_selections[(current_action - 1) // 3]
                            current_card = action[0]
                            current_lane = action[1]
                            core_funct.damage_enemy(current_lane, enemy_position_matrix, enemies, current_card.damage)

                    elif sequence_index == 1:
                        # moving enemies
                        for lane in range(3):
                            enemies = core_funct.move_enemy(lane, 1, 1, enemies, enemy_position_matrix)

                    elif sequence_index == 2:
                        # creating additional enemies
                        core_funct.generate_enemies(enemies, 1, enemy_position_matrix)

                    current_action += 1
                    action_start_time = current_time
            else:
                turn_ended = False
                current_action = 1
                cards_to_modify = []
                for move in move_selections:
                    cards_to_modify.append(cards.index(move[0]))
                core_funct.modify_card_list(cards, cards_to_modify)
                move_selections = []

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((102, 140, 255))

        # draw "end turn" button
        pygame.draw.rect(screen, "white", start_turn_btn)
        screen.blit(render_btn_font, start_turn_btn_position)

        # drawing amnesia meter
        for item in meter:
            item.draw(screen)

        # drawing spots/columns
        for col in spots:
            pygame.draw.rect(screen, "black", col, constants.BORDER_THICKNESS)

        # drawing lanes/rows
        for i, lane in enumerate(lanes):
            if i == selected_lane and selected_lane is not None:
                pygame.draw.rect(screen, "red", lane, constants.BORDER_THICKNESS)
            else:
                pygame.draw.rect(screen, "black", lane, constants.BORDER_THICKNESS)

        # updates enemy list and matrix
        for enemy in enemies[:]:
            if enemy.health <= 0:
                enemies.remove(enemy)
                for lane_index, lane_positions in enumerate(enemy_position_matrix):
                    for index, position in enumerate(lane_positions):
                        if enemy.position == position:
                            enemy_position_matrix[lane_index][index][2] = False

        # drawing enemies
        for enemy in enemies:
            enemy.draw(screen)

        # drawing cards
        for card in cards:
            card.draw(screen)

        if len(move_selections) > 0:
            for move in move_selections:
                move[0].draw_lane_font(screen, move[1])

        # card return to it's spot animation
        if returning_card and card_animation_index < len(returning_path):
            returning_card.update_position(*returning_path[card_animation_index])
            card_animation_index += 1
            if card_animation_index >= len(returning_path):
                returning_card = None

        # GAME RENDERING
        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
