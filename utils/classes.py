import pygame
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
        # x and y coordinates adjusted by entity width
        self.x_cord = x_cord - self.enemy_width / 2
        self.y_cord = y_cord - self.enemy_height / 2
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
        self.x_cord = self.position[0] - self.enemy_width / 2
        self.y_cord = self.position[1] - self.enemy_height / 2


# Card class
class Card:
    card_width = 120
    card_height = 250
    click_color = "dark grey"
    type = None
    assigned_lane = None
    damage = 0

    # create a font object
    card_type_font = pygame.font.Font(None, 36)
    card_lane_match_font = pygame.font.Font(None, 26)

    def __init__(self, x_cord, y_cord, color):
        self.x_cord = x_cord + constants.MARGIN
        self.y_cord = constants.MARGIN
        self.color = color
        self.original_x = self.x_cord
        self.original_y = self.y_cord
        # this variable is not used, might not need it in the future, function parameter needs to
        # go, in that case
        self.y_cord2 = y_cord

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x_cord, self.y_cord, self.card_width, self.card_height))

        # create a font surface object by using font object and text we want to render
        type_text_surface = self.card_type_font.render(str(self.type), False, (0, 0, 0))
        # center text surface object rectangle in a center
        type_text_rect_position = type_text_surface.get_rect(center=(self.x_cord + self.card_width // 2, self.y_cord +
                                                                     self.card_height // 2))
        canvas.blit(type_text_surface, type_text_rect_position)

        if self.assigned_lane is not None:
            # create a font surface for card lane selection
            card_lane_text_surface = self.card_lane_match_font.render(f"Lane: {self.assigned_lane}", False, "black")
            # position text surface object rectangle in a center
            card_lane_rect_position = card_lane_text_surface.get_rect(center=(self.x_cord + self.card_width // 2,
                                                                              self.y_cord + self.card_height // 2 + 50))
            canvas.blit(card_lane_text_surface, card_lane_rect_position)

    def update_position(self, x, y):
        self.x_cord = x
        self.y_cord = y
