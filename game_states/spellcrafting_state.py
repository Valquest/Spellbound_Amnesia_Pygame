import pygame

from variables import constants
from classes import stones


class SpellCrafting:
    def __init__(self, game_instance, screen):
        # import modules
        from classes import util_classes

        # CORE VARIABLES
        # game variables
        self.game_instance = game_instance
        self.screen = screen

        # button variables
        self.home_btn = util_classes.Button(
            "Home Base", 25, constants.WINDOW_HEIGHT - 75, 150, 50, 32)
        self.fusion_btn = util_classes.Button(
            "Start Fusion", constants.WINDOW_WIDTH / 2 + 200, constants.WINDOW_HEIGHT - 75, 200, 50, 32)
        self.spellcraft_btn = util_classes.Button(
            "Craft Spell", constants.WINDOW_WIDTH / 2 + 200, constants.WINDOW_HEIGHT - 130, 200, 50, 32)
        self.reset_ingredients_btn = util_classes.Button(
            "Reset Ingredients", constants.WINDOW_WIDTH / 2 + 420, constants.WINDOW_HEIGHT - 130, 200, 50, 32)

        # stone inventory variables
        self.player_inv = stones.PlayerInventory()
        self.inv = stones.StoneInventory(self.player_inv)
        self.player_inv.spellcraft_instance = self.inv
        self.stones = self.inv.magic_stones

        # mortar instance
        self.mortar = stones.Mortar(self.player_inv, self.inv)

    def update(self) -> None:
        """
        Handles any updates inside of this game class.
        :return: None
        """
        self.inv.apply_scroll_velocity()
        self.inv.check_spring_back_activation()
        self.inv.apply_spring_back()
        self.inv.move_stone()
        self.inv.stone_fall(self.mortar)

    def draw(self) -> None:
        """
        Handles any drawing inside of this game class.
        :return: None
        """
        self.screen.fill((55, 21, 133))
        self.draw_buttons()
        self.draw_inv_side_bar()
        self.draw_mortar()

    def handle_event(self, event) -> None:
        """
        Handles any pygame events inside of this game class.
        :return: None
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button not in (4, 5):
            self.button_clicks()
            self.inv.releasing_stone()
        elif event.type == pygame.MOUSEWHEEL:
            self.inv.scroll_velocity += event.y * self.inv.scroll_speed
            # reset spring back active on new scroll
            self.inv.spring_back_active = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button not in (4, 5):
            # when player uses his mouse to move stone from inventory
            self.inv.select_stone()
        elif event.type == pygame.MOUSEMOTION:
            self.inv.get_mouse_speed(event.rel)

    """_____________ SUPPORT FUNCTIONS _____________"""
    def draw_buttons(self) -> None:
        """
        Handles drawing any buttons.
        :return: None
        """
        # draw home button
        self.home_btn.draw(self.screen)
        self.screen.blit(self.home_btn.font_render, self.home_btn.btn_position)
        self.fusion_btn.draw(self.screen)
        self.screen.blit(self.fusion_btn.font_render, self.fusion_btn.btn_position)
        self.spellcraft_btn.draw(self.screen)
        self.screen.blit(self.spellcraft_btn.font_render, self.spellcraft_btn.btn_position)
        self.reset_ingredients_btn.draw(self.screen)
        self.screen.blit(self.reset_ingredients_btn.font_render, self.reset_ingredients_btn.btn_position)

    def button_clicks(self) -> None:
        """
        Handles catching any bottn click events.
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.home_btn.colided(mouse_pos):
            self.game_instance.current_state = "HomeBase"
        if self.fusion_btn.colided(mouse_pos):
            self.mortar.stone_fusion()
        if self.spellcraft_btn.colided(mouse_pos):
            self.mortar.spell_crafting()
        if self.reset_ingredients_btn.colided(mouse_pos):
            for ingredient in self.mortar.ingredients:
                self.player_inv.add_stone(ingredient.stone_type, ingredient)
            self.mortar.ingredients = []

    def draw_inv_side_bar(self) -> None:
        """
        Handles drawing players inventory sidebar and items.
        :return: None
        """
        self.inv.draw(self.screen)
        # Draw only the parts of the circles that are within the display rectangle
        for stone in self.inv.magic_stones:
            # Check if stone is selected and being moved, then draw that circle anywhere
            if (stone in self.inv.selected_stones or
                    any(falling_stone[0] == stone for falling_stone in self.inv.falling_stones)):
                stone.draw(self.screen)
                continue

            # Calculate the intersection rectangle between the inventory and the stone circle's bounding rect
            stone_rect = pygame.Rect(stone.center[0] - stone.radius, stone.center[1] - stone.radius,
                                     2 * stone.radius, 2 * stone.radius)
            intersection_rect = self.inv.rect.clip(stone_rect)

            if intersection_rect.width > 0 and intersection_rect.height > 0:
                # Create a new surface to hold the visible part of the circle
                result_surface = pygame.Surface((intersection_rect.width, intersection_rect.height), pygame.SRCALPHA)

                # Calculate the area of the stone image to blit
                stone_image_area = pygame.Rect(
                    intersection_rect.x - stone_rect.x,
                    intersection_rect.y - stone_rect.y,
                    intersection_rect.width,
                    intersection_rect.height
                )

                # Blit the part of the stone image that is within the intersection rectangle
                result_surface.blit(stone.image, (0, 0), stone_image_area)

                # Blit the result surface onto the screen
                self.screen.blit(result_surface, intersection_rect.topleft)

                # Calculate the position for the font
                font_position = (stone.center[0] + stone.radius - 20, stone.center[1] + stone.radius - 10)

                # Calculate the intersection rectangle for the font
                font_intersection_rect = self.inv.rect.clip(pygame.Rect(font_position, stone.font_render.get_size()))

                if font_intersection_rect.width > 0 and font_intersection_rect.height > 0:
                    # Create a new surface to hold the visible part of the font
                    font_result_surface = pygame.Surface((font_intersection_rect.width, font_intersection_rect.height),
                                                         pygame.SRCALPHA)

                    # Calculate the area of the font image to blit
                    font_image_area = pygame.Rect(
                        font_intersection_rect.x - font_position[0],
                        font_intersection_rect.y - font_position[1],
                        font_intersection_rect.width,
                        font_intersection_rect.height
                    )

                    # Blit the part of the font image that is within the intersection rectangle
                    font_result_surface.blit(stone.font_render, (0, 0), font_image_area)

                    # Blit the font result surface onto the screen
                    self.screen.blit(font_result_surface, font_intersection_rect.topleft)

    def draw_mortar(self):
        self.mortar.draw(self.screen)
