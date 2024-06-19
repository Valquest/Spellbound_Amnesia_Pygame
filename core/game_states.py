import pygame

from variables import constants, variables


class Game:
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Spellbound Amnesia')

    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.current_state = "Main menu"
        self.battle = Battle(None)
        self.main_menu = MainMenu()

    def run(self):
        while self.running:
            self.event_handler()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

    def event_handler(self):
        # poll for events
        # pygame.Quit event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False




    def update(self):
        match self.current_state:
            case "Main menu":
                self.home_screen.run()
            case "Battlefield":
                self.battle.run()
            case _:
                pass

    def render(self):
        # GAME RENDERING
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill((102, 140, 255))
        # flip() the display to put your work on screen
        pygame.display.flip()

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state

class Battle:
    def __init__(self, event):

    def run(self):
        # when player health goes to 0 quit
        if variables.player_health <= 0:
            self.running = False

        # when mouse button is clicked, get mouse position
        if event.type == pygame.MOUSEBUTTONDOWN:
            # selects a rectangle that is associated with a card class instance
            self.card_selection()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.card_on_lane_selection()

        elif event.type == pygame.MOUSEMOTION:
            self.update_card_position()

        current_time = pygame.time.get_ticks()
        self.battle_actions()

        # setup new frame
        self.draw()

    def card_selection(self):
        # for each card checks if mouse button is pushed down when hovering on a card. Selects that card and
        # stores it to a variable
        for card in cards:
            if pygame.Rect(card.x_cord, card.y_cord, card.card_width, card.card_height).collidepoint(
                    event.pos):
                selected_card = card
                card_offset_x = card.x_cord - event.pos[0]
                card_offset_y = card.y_cord - event.pos[1]
                break

    def card_on_lane_selection(self):
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

    def update_card_position(self):
        if selected_card:
            selected_card.update_position(event.pos[0] + card_offset_x, event.pos[1] + card_offset_y)

    def battle_actions(self):
        # turn based action logic, every action takes 2 seconds to complete, 3 seconds delay between turns
        if turn_ended:
            if current_action <= total_actions * 3:  # Ensure to perform all actions 3 times
                if current_time - action_start_time > delay_between_actions:
                    sequence_index = (current_action - 1) % 3  # Cycle through 0, 1, 2
                    # if player health reaches 0, exit this loop, so that the game could end
                    if variables.player_health <= 0:
                        return
                    if sequence_index == 0:
                        # damaging enemies
                        if (current_action - 1) // 3 < len(move_selections):
                            action = move_selections[(current_action - 1) // 3]
                            current_card = action[0]
                            current_lane = action[1]
                            current_card.cast_effect(battlefield, current_lane, enemies)
                            util_funct.increment_amnesia_bar(meters)

                    elif sequence_index == 1:
                        # Moving enemies
                        for lane_index in range(3):
                            lane = battlefield.lanes[lane_index]
                            enemies_to_move = sorted(lane.get_enemy_list(), reverse=True)
                            for enemy_index in enemies_to_move:
                                positions = battlefield.lanes[lane_index].positions
                                if positions[enemy_index].enemy.frozen > 0:
                                    continue  # Skip frozen enemies
                                final_position_index = enemy_index + 1
                                final_position = positions[final_position_index] if final_position_index < len(
                                    positions) else None
                                spells.move_enemy(enemy_index, lane_index, 1, 1, battlefield)
                                if final_position is None and positions[enemy_index].enemy is None:
                                    player_health.remove_hp()

                    elif sequence_index == 2:
                        # creating additional enemies
                        battlefield.hoard.create_enemy(1)

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

    def draw():

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

class Base:
    def __init__():


class InGameMenu:
    def __init__():


class MainMenu:
    def __init__():


class SpellCrafting:
    def __init__():
