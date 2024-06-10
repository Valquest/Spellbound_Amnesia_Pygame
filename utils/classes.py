import pygame
import random
from variables import constants

pygame.font.init()


# Position class
class Position:
    width = constants.WINDOW_WIDTH / 12.5
    height = constants.WINDOW_HEIGHT / 5 - constants.BORDER_THICKNESS
    enemy = None

    def __init__(self, x, y, occupied=False):
        self.x = x
        self.y = y
        self.occupied = occupied
        self.rect = pygame.Rect(x, y, Position.width, Position.height)


class Lane:
    start_x = constants.WINDOW_WIDTH - constants.MARGIN - Position.width
    # start_x = constants.WINDOW_WIDTH / 10.75 * 4 This starts row reading left to right
    start_y = constants.WINDOW_HEIGHT / 5.1 * 2

    def __init__(self, lane_index):
        self.positions = []
        self.lane_index = lane_index
        for position_index in range(constants.POSITION_NUMBER):
            x_pos = self.start_x - ((Position.width - constants.BORDER_THICKNESS) * position_index + 1)
            y_pos = self.start_y + ((Position.height - constants.BORDER_THICKNESS) * self.lane_index)
            position = Position(x_pos, y_pos)
            self.positions.append(position)


class Battlefield:
    def __init__(self, lane_count):
        self.lanes = []
        for lane_index in range(lane_count):
            lane = Lane(lane_index)
            self.lanes.append(lane)

    def draw(self, canvas):
        for lane in self.lanes:
            for position in lane.positions:
                pygame.draw.rect(canvas, "black", position.rect, constants.BORDER_THICKNESS)


# Enemy class
class Enemy:
    enemy_width = 50
    enemy_height = 50
    position = []
    health = 1

    # create a font object
    enemy_health_font = pygame.font.Font(None, 36)

    def __init__(self, x_cord, y_cord, color):
        # x and y coordinates adjusted by entity width
        self.x_cord = x_cord - self.enemy_width / 2
        self.y_cord = y_cord - self.enemy_height / 2
        self.color = color
        print(f"Enemy created at ({self.x_cord}, {self.y_cord}) with color {self.color}")

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


# hoard class generates enemy instances
class Hoard:
    def __init__(self, temp_var_num_of_enemies, battlefield):
        self.enemy_count = temp_var_num_of_enemies
        self.enemy_list = []
        for _ in range(self.enemy_count):
            # generate random light color for enemies
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            # randomise a row to generate enemy in
            self.random_lane = random.randint(0, constants.LANE_NUMBER - 1)
            lane = battlefield.lanes[self.random_lane]
            for index, position in enumerate(lane.positions):
                if not position.occupied:
                    position = lane.positions[index]
                    center_x, center_y = position.rect.center
                    enemy = Enemy(center_x, center_y, self.color)
                    position.enemy = enemy
                    position.occupied = True
                    # enemy.position = enemy_matrix[random_row][index]
                    enemy.health = random.randint(1, 3)
                    self.enemy_list.append(enemy)
                    break
        print(f"{len(self.enemy_list)} enemies created.")


# Card class
class Card:
    card_width = 120
    card_height = 250
    click_color = "dark grey"
    type = None
    damage = 0
    position = []
    enemy_to_damage = 0

    # create a font object
    card_type_font = pygame.font.Font(None, 32)
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

    def draw_lane_font(self, canvas, assigned_lane):
        # create a font surface for card lane selection
        card_lane_text_surface = self.card_lane_match_font.render(f"Lane: {assigned_lane + 1}", False, "black")
        # position text surface object rectangle in a center
        card_lane_rect_position = card_lane_text_surface.get_rect(center=(self.x_cord + self.card_width // 2,
                                                                          self.y_cord + self.card_height // 2 + 50))
        canvas.blit(card_lane_text_surface, card_lane_rect_position)

    def update_position(self, x, y):
        self.x_cord = x
        self.y_cord = y


# amnesia meter class
class Meter:
    width = 20
    height = 20

    def __init__(self, x_pos, border=False):
        from variables import variables
        self.border = border
        self.x_pos = x_pos
        self.y_pos = variables.amnesia_bar_y
        self.rect_obj = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw(self, screen):
        if self.border:
            pygame.draw.rect(screen, "blue", self.rect_obj, constants.BORDER_THICKNESS)
        else:
            pygame.draw.rect(screen, "blue", self.rect_obj)


# any button class
class Button:
    start_btn_font = pygame.font.Font(None, 32)

    def __init__(self, button_name, x_pos, y_pos, width, height):
        self.name = button_name
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font_render = self.start_btn_font.render("Start Turn", True, (0, 0, 0))
        self.btn_position = self.font_render.get_rect(center=((Card.card_width + constants.MARGIN) *
                                                              constants.CARD_COUNT + 100 + 200 // 2,
                                                              constants.MARGIN + 50 // 2))

    # draw a button
    def draw(self, canvas):
        pygame.draw.rect(canvas, "white", self.rect)
