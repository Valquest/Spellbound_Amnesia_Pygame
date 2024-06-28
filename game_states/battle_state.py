import pygame

from variables import constants, variables

"""
This is a battle state module. It stores all the needed functionality for battles to work.
"""


class Battle:
    def __init__(self, game_instance, screen):

        # local imports
        from core import core_funct
        from utils import util_funct
        from classes import util_classes
        from classes import battle_classes

        # core class instances initiated
        self.battlefield = battle_classes.Battlefield(constants.LANE_NUMBER)
        self.cards = core_funct.create_card_list()
        self.meters = util_funct.add_amnesia_bar(constants.AMNESIA_BAR_COUNT)

        # CORE VARIABLES
        # action variables
        self.action_start_time = 0
        self.current_action = 1
        self.delay_between_actions = 1000
        self.move_selections = []
        self.total_actions = 3
        self.turn_ended = False

        # button variables
        self.start_turn_btn = util_classes.Button(
            "Start turn",
            (battle_classes.Card.card_width + constants.MARGIN) * constants.CARD_COUNT + 150 // 2,
            constants.MARGIN + 25 // 2, 200, 50, 32)
        self.home_button = util_classes.Button(
            "Home Base", 25, constants.WINDOW_HEIGHT - 75, 100, 50, 32)

        # card variables
        self.card_animation_index = 0
        self.card_offset_x = 0
        self.card_offset_y = 0
        self.returning_card = None
        self.returning_path = []
        self.selected_card = None

        # enemy variables
        self.enemies = self.battlefield.hoard.enemy_list

        # game variables
        self.game_instance = game_instance
        self.screen = screen
        self.running = game_instance.running

        # player health variables
        self.player_health = battle_classes.PlayerHealth()
        self.health_crystals = self.player_health.crystal_list

    def update(self):
        self.battle_actions()

    def battle_actions(self):
        from utils import util_funct
        from core import core_funct, spells

        current_time = pygame.time.get_ticks()

        # turn based action logic, every action takes 2 seconds to complete, 3 seconds delay between turns
        if self.turn_ended:
            if self.current_action <= self.total_actions * 3:  # Ensure to perform all actions 3 times
                if current_time - self.action_start_time > self.delay_between_actions:
                    sequence_index = (self.current_action - 1) % 3  # Cycle through 0, 1, 2
                    # if player health reaches 0, exit this loop, so that the game could end
                    if variables.player_health <= 0:
                        self.game_instance.current_state = "HomeBase"
                    if sequence_index == 0:
                        # damaging enemies
                        if (self.current_action - 1) // 3 < len(self.move_selections):
                            action = self.move_selections[(self.current_action - 1) // 3]
                            current_card = action[0]
                            current_lane = action[1]
                            current_card.cast_effect(self.battlefield, current_lane, self.enemies)
                            util_funct.increment_amnesia_bar(self.meters)

                    elif sequence_index == 1:
                        # Moving enemies
                        for lane_index in range(3):
                            lane = self.battlefield.lanes[lane_index]
                            enemies_to_move = sorted(lane.get_enemy_list(), reverse=True)
                            for enemy_index in enemies_to_move:
                                positions = self.battlefield.lanes[lane_index].positions
                                final_position_index = enemy_index + 1
                                final_position = positions[final_position_index] if final_position_index < len(
                                    positions) else None
                                spells.move_enemy(enemy_index, lane_index, 1, 1, self.battlefield)
                                if final_position is None and positions[enemy_index].enemy is None:
                                    self.player_health.remove_hp()

                    elif sequence_index == 2:
                        # creating additional enemies
                        self.battlefield.hoard.create_enemy(1)

                    self.current_action += 1
                    self.action_start_time = current_time
            else:
                self.turn_ended = False
                self.current_action = 1
                cards_to_modify = [self.cards.index(move[0]) for move in self.move_selections]
                core_funct.modify_card_list(self.cards, cards_to_modify)
                self.move_selections = []

    def button_clicks(self):

        # if "start turn" button is collided with mouse position
        if self.start_turn_btn.colided(pygame.mouse.get_pos()):
            # end the turn by changing flag and mark down game time during the click
            self.turn_ended = True
            self.action_start_time = pygame.time.get_ticks()

        if self.home_button.colided(pygame.mouse.get_pos()):
            self.game_instance.current_state = "HomeBase"

    def card_on_lane_selection(self):
        from core import core_funct
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        if self.selected_card:
            for lane in self.battlefield.lanes:
                lane_index = None
                # check if there are any enemies on that lane, if no, prevent selection
                enemies_on_lane = []
                for position in lane.positions:
                    if position.enemy:
                        enemies_on_lane.append(position.enemy)
                # add card and lane to move selection list
                for position in lane.positions:
                    if position.rect.collidepoint(mouse_pos) and enemies_on_lane:
                        lane_index = self.battlefield.lanes.index(lane)

                        # Check if the selected card is already in move_selections
                        card_in_moves = any(selection[0] == self.selected_card for selection in self.move_selections)

                        # Clear the move selections list if the card is already present or if it already has 3 entries
                        if card_in_moves or len(self.move_selections) >= 3:
                            self.move_selections.clear()

                        # Add the new card and lane index entry at the end of the list
                        self.move_selections.append([self.selected_card, lane_index])
                        break

            # Calculate returning path
            self.returning_path = core_funct.calculate_return_path(
                (self.selected_card.x_cord, self.selected_card.y_cord),
                (self.selected_card.original_x, self.selected_card.original_y))
            self.returning_card = self.selected_card
            self.card_animation_index = 0
            self.selected_card = None

    def card_selection(self, event):
        # for each card checks if mouse button is pushed down when hovering on a card. Selects that card and
        # stores it to a variable
        for card in self.cards:
            card_rect = pygame.Rect(card.x_cord, card.y_cord, card.card_width, card.card_height)
            if pygame.Rect(card.x_cord, card.y_cord, card.card_width, card.card_height).collidepoint(
                    event.pos):
                self.selected_card = card
                self.card_offset_x = card.x_cord - event.pos[0]
                self.card_offset_y = card.y_cord - event.pos[1]
                break

    def draw(self):

        self.screen.fill((102, 140, 255))

        self.draw_buttons()

        # drawing health crystals
        for crystal in self.health_crystals:
            crystal.draw(self.screen)

        # drawing amnesia meter
        for item in self.meters:
            item.draw(self.screen)

        # draw positions
        self.battlefield.draw(self.screen)

        # drawing enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # drawing cards
        for card in self.cards:
            card.draw(self.screen)

        # draw card lane selection fonts
        if len(self.move_selections) > 0:
            for index, move in enumerate(self.move_selections):
                move[0].draw_lane_font(self.screen, move[1])
                move[0].draw_card_turn_text(self.screen, index)

        # card return to it's spot animation
        if self.returning_card and self.card_animation_index < len(self.returning_path):
            self.returning_card.update_position(*self.returning_path[self.card_animation_index])
            self.card_animation_index += 1
            if self.card_animation_index >= len(self.returning_path):
                returning_card = None

    def draw_buttons(self):

        # draw "start turn" button
        self.start_turn_btn.draw(self.screen)
        self.screen.blit(self.start_turn_btn.font_render, self.start_turn_btn.btn_position)

        # draw home button
        self.home_button.draw(self.screen)
        self.screen.blit(self.home_button.font_render, self.home_button.btn_position)

    def handle_event(self, event):
        if variables.player_health <= 0:
            self.game_instance.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.card_selection(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.card_on_lane_selection()
            self.button_clicks()
        elif event.type == pygame.MOUSEMOTION:
            self.update_card_position(event)

    def update_card_position(self, event):
        if self.selected_card:
            self.selected_card.update_position(event.pos[0] + self.card_offset_x, event.pos[1] + self.card_offset_y)