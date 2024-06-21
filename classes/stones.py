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

    def draw(self, canvas):
        pygame.draw.rect(canvas, "White", self.rect)


class StoneInventory:
    def __init__(self):

        # CORE VARIABLES
        # rect variables
        self.x = 100
        self.y = 200
        self.width = constants.INVENTORY_WIDTH
        self.height = constants.INVENTORY_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # magic stone variables
        self.magic_stones = []
        for stone_data in entities.stone_types:
            stone = MagicStone(stone_data[0], stone_data[1][0], stone_data[1][1], self.x + self.width / 2, )
            for stone_ammount in entities.player_inv:
                stone.ammount = [ammount for stone_type, ammount in stone_ammount if stone_data[0] == stone_type]
            self.magic_stones.append(stone)

    def draw(self, canvas):
        pygame.draw.rect(canvas, "Gray", self.rect)
