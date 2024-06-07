import pygame
import random
from variables import constants

pygame.font.init()


# Enemy class
class Enemy:
    enemy_width = 50
    enemy_height = 50
    position = []
    health = 1

    # create a font object
    enemy_health_font = pygame.font.Font(None, 36)

    def __init__(self, y_cord, x_cord, color):
        # self.position = [x_cord, y_cord, True]
        # self.x_cord = self.position[0]
        # self.y_cord = self.position[1]
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x_cord, self.y_cord, self.enemy_width, self.enemy_height))

        # create a font surface object by using font object and text we want to render
        text_surface_object = self.enemy_health_font.render(str(self.health), False, (0, 0, 0))

        # center text surface object rectangle in a center
        text_rect_position = text_surface_object.get_rect(center=(self.x_cord + self.enemy_width // 2, self.y_cord +
                                                                  self.enemy_height // 2))

        canvas.blit(text_surface_object, text_rect_position)

    def update_position(self):
        self.x_cord = self.position[0]  # Update x-cord from position[0]
        self.y_cord = self.position[1]  # Update y-cord from position[1]
        print("positions updated")

# Card class
class Card:
    card_width = 120
    card_height = 250
    click_color = "dark grey"
    type = None

    # create a font object
    card_type_font = pygame.font.Font(None, 36)

    def __init__(self, x_cord, y_cord, color):
        self.x_cord = x_cord + constants.MARGIN
        self.y_cord = constants.MARGIN
        self.color = color
        self.original_x = self.x_cord
        self.original_y = self.y_cord

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x_cord, self.y_cord, self.card_width, self.card_height))

        # create a font surface object by using font object and text we want to render
        text_surface_object = self.card_type_font.render(str(self.type), False, (0, 0, 0))

        # center text surface object rectangle in a center
        text_rect_position = text_surface_object.get_rect(center=(self.x_cord + self.card_width // 2, self.y_cord +
                                                                  self.card_height // 2))

        canvas.blit(text_surface_object, text_rect_position)

    def update_position(self, x, y):
        self.x_cord = x
        self.y_cord = y
