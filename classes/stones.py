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
        self.x = 5
        self.y = 100
        self.width = constants.INVENTORY_WIDTH
        self.height = constants.INVENTORY_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # inv scroll variables
        self.scroll_speed = 5
        self.scroll_velocity = 0
        self.deceleration = 0.94
        self.min_velocity = 0.01
        self.tiny_increment_threshold = self.min_velocity
        self.tiny_increment_deceleration = 0.999

        # magic stone variables
        self.magic_stones = []
        for index, (stone_name, stone_attributes) in enumerate(entities.stone_types.items()):
            stone = MagicStone(stone_name, stone_attributes["rarity"], stone_attributes["image_name"],
                               self.x + self.width / 2 - 30 / 2, self.y + 40 + (45 * index), 30, 30)
            for stone_type, ammount in entities.player_inv.items():
                if stone_name == stone_type:
                    stone.ammount = ammount
                    break
            self.magic_stones.append(stone)

    def draw(self, screen):
        pygame.draw.rect(screen, "Gray", self.rect)
        # Draw large rectangle
        pygame.draw.rect(screen, "Black", self.rect, 2)

        # Draw only the parts of the rectangles that are within the display rectangle
        for stones in self.magic_stones:
            intersection_rect = self.rect.clip(stones)

            if intersection_rect.width > 0 and intersection_rect.height > 0:
                # Create a new surface to hold the visible part of the rectangle
                result_surface = pygame.Surface((intersection_rect.width, intersection_rect.height))
                result_surface.fill("Black")

                # Blit the part of the rectangle that is within the intersection rectangle
                screen.blit(result_surface, intersection_rect.topleft)

    def scroll(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_velocity += event.y * self.scroll_speed

    def update(self):
        # Apply scroll velocity
        if abs(self.scroll_velocity) > self.min_velocity:
            for stones in self.magic_stones:
                stones.y += self.scroll_velocity
            # Use a less aggressive deceleration for tiny increments
            if abs(self.scroll_velocity) < self.tiny_increment_threshold:
                self.scroll_velocity *= self.tiny_increment_deceleration
            else:
                self.scroll_velocity *= self.deceleration
