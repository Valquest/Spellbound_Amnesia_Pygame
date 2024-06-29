import pygame


class HomeBase:

    def __init__(self, game_instance, screen):
        # import modules
        from classes import util_classes

        # CORE VARIABLES
        # game variables
        self.game_instance = game_instance
        self.screen = screen

        # button variables
        self.to_battle_btn = util_classes.Button(
            "To Battle!", 25, 75, 150, 50, 32)
        self.spell_crafting_btn = util_classes.Button(
            "Craft Spells", 25, 150, 150, 50, 32)

    @staticmethod
    def update(self) -> None:
        """
        To be populated.
        :return: None
        """
        x = 0

    def draw_buttons(self) -> None:
        """
        Handles drawing buttons for this game state.
        :return: None
        """
        # draw "to battle" button
        self.to_battle_btn.draw(self.screen)
        self.screen.blit(self.to_battle_btn.font_render, self.to_battle_btn.btn_position)

        # draw "spell crafting" button
        self.spell_crafting_btn.draw(self.screen)
        self.screen.blit(self.spell_crafting_btn.font_render, self.spell_crafting_btn.btn_position)

    def button_clicks(self) -> None:
        """
        Handles game state changes.
        :return: None
        """
        if self.to_battle_btn.colided(pygame.mouse.get_pos()):
            self.game_instance.current_state = "Battlefield"
        if self.spell_crafting_btn.colided(pygame.mouse.get_pos()):
            self.game_instance.current_state = "SpellCrafting"

    def draw(self) -> None:
        """
        Does all the drawing in this game state.
        :return: None
        """
        self.screen.fill((45, 166, 59))
        self.draw_buttons()

    def handle_event(self, event) -> None:
        """
        Handles pygame events for this game state.
        :return: None
        """
        if event.type == pygame.MOUSEBUTTONUP:
            self.button_clicks()
