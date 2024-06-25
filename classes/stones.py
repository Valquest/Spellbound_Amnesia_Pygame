import pygame

from data import entities
from variables import constants


class MagicStone:
    def __init__(self, stone_type, rarity, image_name, x_pos, y_pos, width, height):

        # CORE VARIABLES
        # stone variables
        self.stone_type = stone_type
        self.rarity = rarity
        self.image_name = image_name
        self.ammount = 0

        # rectangle variables
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect_color = "White"

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.rect_color, self.rect)


class StoneInventory:
    def __init__(self):

        # CORE VARIABLES
        # rect variables
        self.x = 50
        self.y = 100
        self.width = constants.INVENTORY_WIDTH
        self.height = constants.INVENTORY_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # scroll settings
        self.scroll_speed = 5
        self.scroll_velocity = 0
        self.deceleration = 0.94
        self.min_velocity = 0.01
        self.tiny_increment_threshold = self.min_velocity
        self.tiny_increment_deceleration = 0.999
        self.max_scroll_offset = 100
        self.padding = 10

        # Hard scroll limits
        self.scroll_limit_distance = 70
        self.top_hard_limit = self.rect.top + self.scroll_limit_distance
        self.bottom_hard_limit = self.rect.bottom - self.scroll_limit_distance

        # Spring back settings
        self.spring_back_active = False
        self.spring_back_speed = 2
        self.target_offset = 0

        # magic stone variables
        self.magic_stones = []
        for index, (stone_name, stone_attributes) in enumerate(entities.stone_types.items()):
            stone = MagicStone(stone_name, stone_attributes["rarity"], stone_attributes["image_name"],
                               self.x + self.width / 2 - 30 / 2, self.y + 20 + (45 * index), 30, 30)
            for stone_type, ammount in entities.player_inv.items():
                if stone_name == stone_type:
                    stone.ammount = ammount
                    break
            self.magic_stones.append(stone)

    # drawing main inv rect
    def draw(self, screen):
        pygame.draw.rect(screen, "Gray", self.rect)

    # Function to calculate resistance based on proximity to limits
    @staticmethod
    def calculate_resistance(position, limit, max_offset):
        offset = abs(position - limit)
        if offset > max_offset:
            offset = max_offset
        resistance = (max_offset - offset) / max_offset
        return resistance
