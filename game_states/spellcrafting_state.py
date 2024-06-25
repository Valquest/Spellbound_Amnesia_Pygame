import pygame

from variables import constants, variables
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

        # stone inventory variables
        self.inv = stones.StoneInventory()
        self.stones = self.inv.magic_stones

    def update(self):
        if abs(self.inv.scroll_velocity) > self.inv.min_velocity:
            # Check the position of the topmost and bottommost rectangles
            topmost_rect = self.inv.magic_stones[0].rect
            bottommost_rect = self.inv.magic_stones[-1].rect

            # if scrolling up, ensure the topmost rectangle does not go above the top of the large rectangle
            if self.inv.scroll_velocity > 0 and topmost_rect.top + self.inv.scroll_velocity >= self.inv.rect.top + 20:
                self.inv.scroll_velocity = (
                            self.inv.rect.top - topmost_rect.top) if topmost_rect.top < self.inv.rect.top else 0

            # If scrolling down, ensure the bottommost rectangle does not go below the bottom of the large rectangle
            elif self.inv.scroll_velocity < 0 and bottommost_rect.bottom + self.inv.scroll_velocity <= self.inv.rect.bottom - 20:
                self.inv.scroll_velocity = (
                            self.inv.rect.bottom - bottommost_rect.bottom) if bottommost_rect.bottom > self.inv.rect.bottom else 0

            # print(self.inv.scroll_velocity)
            for stone in self.inv.magic_stones:
                stone.rect.y += self.inv.scroll_velocity

            # Use a less aggressive deceleration for tiny increments
            if abs(self.inv.scroll_velocity) < self.inv.tiny_increment_threshold:
                self.inv.scroll_velocity *= self.inv.tiny_increment_deceleration
            else:
                self.inv.scroll_velocity *= self.inv.deceleration

    def draw_buttons(self):
        # draw home button
        self.home_btn.draw(self.screen)
        self.screen.blit(self.home_btn.font_render, self.home_btn.btn_position)

    def button_clicks(self):
        if self.home_btn.colided(pygame.mouse.get_pos()):
            self.game_instance.current_state = "HomeBase"

    def draw(self):
        self.screen.fill((55, 21, 133))
        self.draw_buttons()
        self.draw_inv_side_bar()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.button_clicks()
        elif event.type == pygame.MOUSEWHEEL:
            self.inv.scroll_velocity += event.y * self.inv.scroll_speed

    def draw_inv_side_bar(self):
        self.inv.draw(self.screen)
        # for stone in self.stones:
        #     stone.draw(self.screen)

        # Draw only the parts of the rectangles that are within the display rectangle
        for stone in self.inv.magic_stones:
            intersection_rect = self.inv.rect.clip(stone.rect)
            if intersection_rect.width > 0 and intersection_rect.height > 0:
                # Create a new surface to hold the visible part of the rectangle
                result_surface = pygame.Surface((intersection_rect.width, intersection_rect.height))
                result_surface.fill(stone.rect_color)

                # Blit the part of the rectangle that is within the intersection rectangle
                self.screen.blit(result_surface, intersection_rect.topleft)
