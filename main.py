import pygame
import random
# project files
from utils import classes
from variables import constants
from core import core_funct
from utils import util_funct
from data import entities


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
                               constants.MARGIN - ((constants.COL_WIDTH - constants.BORDER_THICKNESS) * col) -
                               constants.COL_WIDTH / 2), 0))
            y_pos = int(round((constants.WINDOW_HEIGHT -
                               constants.MARGIN - (constants.LANE_HEIGHT * (3 - row))
                               + constants.LANE_HEIGHT / 2), 0))
            occupied = False
            position = [x_pos, y_pos, occupied]
            row_position.append(position)
        enemy_position_matrix.append(row_position)

    # create lanes/rows
    lanes = util_funct.add_lanes(constants.ROW_NUMBER)

    # create spots/columns
    spots = util_funct.add_columns(constants.COL_NUMBER)

    # generating game cards
    cards = []
    for count in range(constants.CARD_COUNT):
        random_item = random.choice(list(entities.card_types.items()))

        temp_card = classes.Card(150 * count + 1, 0, "gray")

        # take random card type and damage value from the card type dictionary
        temp_card.type = random_item[0]
        temp_card.damage = random_item[1]

        cards.append(temp_card)

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

    # generate an end turn button and text
    end_turn_btn = pygame.Rect((cards[0].card_width + constants.MARGIN) * constants.CARD_COUNT + 100, constants.MARGIN,
                               200, 50)
    turn_ended = False
    end_btn_font = pygame.font.Font(None, 32)
    render_btn_font = end_btn_font.render("Start Turn", True, (0, 0, 0))
    end_turn_btn_position = render_btn_font.get_rect(center=((cards[0].card_width + constants.MARGIN) *
                                                             constants.CARD_COUNT + 100 + 200 // 2, constants.MARGIN +
                                                             50 // 2))

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
    card_select_lane_select = []

    # turn related variables
    total_actions = 3
    current_action = 1
    action_start_time = 0
    delay_between_actions = 1500
    players_turn = True

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
                if end_turn_btn.collidepoint(mouse_pos):
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
                            print(f"Card {cards.index(selected_card)} touched Lane {lanes.index(lane)}")
                            card_select_lane_select.append((selected_card, lanes.index(lane)))
                            selected_card.assigned_lane = lanes.index(lane)
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
            if current_action <= total_actions:
                if current_time - action_start_time > delay_between_actions:

                    # damaging enemies
                    action = card_select_lane_select[current_action - 1]
                    current_card = action[0]
                    current_lane = action[1]
                    core_funct.damage_enemy(current_lane, enemy_position_matrix, enemies, current_card.damage)

                    # create additional enemy
                    core_funct.generate_enemies(enemies, 1, enemy_position_matrix)

                    current_action += 1
                    action_start_time = current_time
                    for action in card_select_lane_select:
                        lane = action[1]
                        enemies = core_funct.move_enemy(lane, 1, 1, enemies, enemy_position_matrix)

            else:
                turn_ended = False
                current_action = 1
                card_select_lane_select = []

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((102, 140, 255))

        # draw "end turn" button
        pygame.draw.rect(screen, "white", end_turn_btn)
        screen.blit(render_btn_font, end_turn_btn_position)

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
