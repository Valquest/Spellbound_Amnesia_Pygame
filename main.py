import pygame
import random

# project files
from utils import classes
from variables import constants, variables
from core import core_funct, spells
from utils import util_funct


def main():
    # pygame setup
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Spellbound Amnesia')

    # generic game variables
    running = True
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    turn_ended = False
    clock = pygame.time.Clock()

    # create battlefield with lanes and positions
    battlefield = classes.Battlefield(constants.LANE_NUMBER)

    # create amnesia meter bar
    meters = util_funct.add_amnesia_bar(constants.AMNESIA_BAR_COUNT)

    # generating game cards
    cards = core_funct.create_card_list()

    # generating player health crystals
    player_health = classes.PlayerHealth()
    health_crystals = player_health.crystal_list

    # generate enemies
    hoard = classes.Hoard(random.randint(4, 8), battlefield)
    enemies = hoard.enemy_list

    # generate a start turn button and text
    start_turn_btn = classes.Button("Start turn", (classes.Card.card_width + constants.MARGIN) *
                                    constants.CARD_COUNT + 100, constants.MARGIN, 200, 50)

    # MAIN GAME LOOP

    # game loop variables
    selected_lane = None
    selected_card = None
    move_selections = []

    # turn related variables
    total_actions = 3
    current_action = 1
    action_start_time = 0
    delay_between_actions = 1000

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
            # when player health goes to 0 quit
            if variables.player_health <= 0:
                running = False
            # when mouse button is clicked, get mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                # for each card checks if mouse button is pushed down when hovering on a card. Selects that card and
                # stores it to a variable
                for card in cards:
                    if pygame.Rect(card.x_cord, card.y_cord, card.card_width, card.card_height).collidepoint(event.pos):
                        selected_card = card
                        card_offset_x = card.x_cord - event.pos[0]
                        card_offset_y = card.y_cord - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                # get mouse position
                mouse_pos = pygame.mouse.get_pos()
                # if "start turn" button is collided with mouse position
                if start_turn_btn.rect.collidepoint(mouse_pos):
                    # end the turn by changing flag and mark down game time during the click
                    turn_ended = True
                    action_start_time = pygame.time.get_ticks()
                if selected_card:
                    for lane in battlefield.lanes:
                        lane_index = None
                        # check if there are any enemies on that lane, if no, prevent selection
                        enemies_on_lane = []
                        for position in lane.positions:
                            if position.enemy:
                                enemies_on_lane.append(position.enemy)
                        # add card and lane to move selection list
                        for position in lane.positions:
                            if position.rect.collidepoint(mouse_pos) and not not enemies_on_lane:
                                lane_index = battlefield.lanes.index(lane)
                                # sets variable move_index to -1 so that further conditions avoid iterating
                                # move_selections if move_index is not set to value above -1
                                move_index = -1
                                print(f"Card {cards.index(selected_card)} touched Lane {lane_index}")
                                # checks if cards that are being selected are not already in the list, if they are, lane
                                # is rewritten on top of the same list item
                                for index, selection in enumerate(move_selections):
                                    if selection[0] == selected_card:
                                        move_index = index
                                        break
                                if move_index != -1:
                                    move_selections[move_index][1] = lane_index
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
                            current_card.cast_effect(battlefield, current_lane, enemies)
                            util_funct.increment_amnesia_bar(meters)

                    elif sequence_index == 1:
                        # moving enemies
                        for lane in range(3):
                            # move enemies and check if move_enemy function simultaneously returns 1
                            if spells.move_enemy(lane, 1, 1, battlefield) == 1:
                                player_health.remove_hp()

                    elif sequence_index == 2:
                        # creating additional enemies
                        hoard.create_enemy(1)

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

        # draw start turn button with text
        start_turn_btn.draw(screen)
        screen.blit(start_turn_btn.font_render, start_turn_btn.btn_position)

        # drawing health crystals
        for crystal in health_crystals:
            crystal.draw(screen)

        # drawing amnesia meter
        for item in meters:
            item.draw(screen)

        # draw positions
        battlefield.draw(screen)

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
