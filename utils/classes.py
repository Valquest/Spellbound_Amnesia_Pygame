import pygame
from variables import constants


# Enemy class
class Enemy:
    enemy_width = 50
    enemy_height = 50
    position = []
    health = 1

    def __init__(self, lane_pos, col_pos, color):
        self.lane_pos = lane_pos
        self.col_pos = col_pos
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.col_pos, self.lane_pos, self.enemy_width, self.enemy_height))


# Card class
class Card:
    card_width = 120
    card_height = 250
    click_color = "dark grey"
    type = None

    def __init__(self, x_cord, y_cord, color):
        self.x_cord = x_cord + constants.MARGIN
        self.y_cord = constants.MARGIN
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x_cord, self.y_cord, self.card_width, self.card_height))
