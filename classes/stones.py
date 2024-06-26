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
        self.padding = 20

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
            for stone_type, amount in entities.player_inv.items():
                if stone_name == stone_type:
                    stone.ammount = amount
                    break
            self.magic_stones.append(stone)

    # drawing main inv rect
    def draw(self, screen):
        pygame.draw.rect(screen, "Gray", self.rect)

        # scrolling logic

    """-------------------------------"""

    def apply_scroll_velocity(self):
        # Ensure scrolling does not exceed hard limits
        if (self.scroll_velocity > 0 and self.magic_stones[0].rect.top >= self.top_hard_limit) or \
                (self.scroll_velocity < 0 and self.magic_stones[-1].rect.bottom <= self.bottom_hard_limit):
            self.scroll_velocity = 0

        if abs(self.scroll_velocity) > self.min_velocity:
            for stone in self.magic_stones:
                stone.rect.y += self.scroll_velocity

            # Deceleration
            if abs(self.scroll_velocity) < self.tiny_increment_threshold:
                self.scroll_velocity *= self.tiny_increment_deceleration
            else:
                self.scroll_velocity *= self.deceleration

            # Hard boundary enforcement during scrolling
            if self.magic_stones[0].rect.top > self.top_hard_limit:
                for stone in self.magic_stones:
                    stone.rect.y = max(
                        stone.rect.y - self.scroll_velocity,
                        self.top_hard_limit + self.magic_stones.index(stone) * (stone.height + 10)
                    )
                self.scroll_velocity = 0
            elif self.magic_stones[-1].rect.bottom < self.bottom_hard_limit:
                for stone in self.magic_stones:
                    stone.rect.y = min(
                        stone.rect.y - self.scroll_velocity,
                        self.bottom_hard_limit - (
                                len(self.magic_stones) - self.magic_stones.index(stone)) * (
                                stone.height + 10)
                    )
                self.scroll_velocity = 0

            # Increase resistance the further you scroll past the limit
            if self.magic_stones[0].rect.top > self.rect.top + self.padding:
                resistance = self.calculate_resistance(
                    self.magic_stones[0].rect.top,
                    self.rect.top + self.padding,
                    self.max_scroll_offset
                )
                self.scroll_velocity *= resistance
            elif self.magic_stones[-1].rect.bottom < self.rect.bottom - self.padding:
                resistance = self.calculate_resistance(
                    self.magic_stones[-1].rect.bottom,
                    self.rect.bottom - self.padding,
                    self.max_scroll_offset
                )
                self.scroll_velocity *= resistance
        else:
            self.scroll_velocity = 0

    def check_spring_back_activation(self):
        if not self.spring_back_active:
            if self.magic_stones[0].rect.top > self.rect.top + self.padding:
                self.target_offset = (self.rect.top + self.padding) - self.magic_stones[0].rect.top
                self.spring_back_active = True
            elif self.magic_stones[-1].rect.bottom < self.rect.bottom - self.padding:
                self.target_offset = (self.rect.bottom - self.padding) - self.magic_stones[
                    -1].rect.bottom
                self.spring_back_active = True

    def apply_spring_back(self):
        if self.spring_back_active:
            spring_back_factor = 1 + abs(self.target_offset) / self.max_scroll_offset
            if self.target_offset > 0:
                resistance = self.calculate_resistance(
                    self.magic_stones[-1].rect.bottom,
                    self.rect.bottom - self.scroll_limit_distance,
                    self.max_scroll_offset
                )
                for stone in self.magic_stones:
                    stone.rect.y += self.spring_back_speed * spring_back_factor * resistance
                if self.magic_stones[-1].rect.bottom >= self.rect.bottom - self.padding:
                    offset = self.magic_stones[-1].rect.bottom - (self.rect.bottom - self.padding)
                    for stone in self.magic_stones:
                        stone.rect.y -= offset
                    self.spring_back_active = False
            elif self.target_offset < 0:
                resistance = self.calculate_resistance(
                    self.magic_stones[0].rect.top,
                    self.rect.top + self.scroll_limit_distance,
                    self.max_scroll_offset
                )
                for stone in self.magic_stones:
                    stone.rect.y -= self.spring_back_speed * spring_back_factor * resistance
                if self.magic_stones[0].rect.top <= self.rect.top + self.padding:
                    offset = (self.rect.top + self.padding) - self.magic_stones[0].rect.top
                    for stone in self.magic_stones:
                        stone.rect.y += offset
                    self.spring_back_active = False

    @staticmethod
    def calculate_resistance(position, limit, max_offset):
        offset = abs(position - limit)
        if offset > max_offset:
            offset = max_offset
        resistance = (max_offset - offset) / max_offset
        return resistance ** 2  # Apply the squared resistance for smoother behavior

    """----------------------------------------"""
