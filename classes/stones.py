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
        self.scroll_y_pos = 0

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

        # hard scroll limits
        self.scroll_limit_distance = 70
        self.top_hard_limit = self.rect.top + self.scroll_limit_distance
        self.bottom_hard_limit = self.rect.bottom - self.scroll_limit_distance

        # spring back settings
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

        # stone movement variables
        self.selected_stone = None
        self.falling_stone = None
        self.mouse_speed = 0
        self.stone_move_velocity = 0
        self.stone_move_acceleration = 10
        self.stone_move_acceleration_increment = 0.2
        self.stone_move_acceleration_multiplier = 0.9
        self.stone_fall_velocity = 0
        self.fall_acceleration = 10
        self.fall_acceleration_increment = 0.2
        self.fall_acceleration_multiplier = 0.9

    # drawing main inv rect
    def draw(self, screen):
        pygame.draw.rect(screen, "Gray", self.rect)

    """---------Scrolling logic---------"""
    def apply_scroll_velocity(self):
        # check if any items are selected or falling, if yes, exit function
        if self.falling_stone or self.selected_stone:
            return
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
        # check if any items are selected or falling, if yes, exit function
        if self.falling_stone or self.selected_stone:
            return
        if not self.spring_back_active:
            if self.magic_stones[0].rect.top > self.rect.top + self.padding:
                self.target_offset = (self.rect.top + self.padding) - self.magic_stones[0].rect.top
                self.spring_back_active = True
            elif self.magic_stones[-1].rect.bottom < self.rect.bottom - self.padding:
                self.target_offset = (self.rect.bottom - self.padding) - self.magic_stones[
                    -1].rect.bottom
                self.spring_back_active = True

    def apply_spring_back(self):
        # check if any items are selected or falling, if yes, exit function
        if self.falling_stone or self.selected_stone:
            return
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

    """----------Moving Stones logic-----------"""

    def select_stone(self) -> None:
        """
        Assigns a stone to stone_in_motion variable when player selects a stone with mouse
        :return: None
        """
        if self.falling_stone:
            return
        for stone in self.magic_stones:
            if stone.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected_stone = stone
        # set scroll velocity to 0 to prevent bug where scrolling happens on item return to inv
        self.scroll_velocity = 0

    # def move_stone(self) -> None:
    #     """
    #     Moves selected stone to current mouse position while stone in motion is selected
    #     :return: None
    #     """
    #     if self.selected_stone:
    #         mouse_pos = pygame.mouse.get_pos()
    #         stone_width = self.selected_stone.width
    #         stone_height = self.selected_stone.height
    #         x_direction = self.selected_stone.rect.x
    #         self.selected_stone.rect.x = mouse_pos[0] - stone_width / 2
    #         self.selected_stone.rect.y = mouse_pos[1] - stone_height / 2

    def move_stone(self) -> None:
        """
        Moves selected stone to current mouse position with acceleration and deceleration
        :return: None
        """
        if self.selected_stone:
            mouse_pos = pygame.mouse.get_pos()
            stone_rect = self.selected_stone.rect
            stone_center_x = stone_rect.x + stone_rect.width / 2
            stone_center_y = stone_rect.y + stone_rect.height / 2

            # Calculate distance to the mouse position
            distance_x = mouse_pos[0] - stone_center_x
            distance_y = mouse_pos[1] - stone_center_y

            # Calculate the distance to the mouse position
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            # Increase velocity based on the distance, with a cap
            max_velocity = 10  # Adjust this value to control max speed
            self.stone_move_velocity = min(self.stone_move_acceleration * distance, max_velocity)

            # Normalize direction and apply velocity
            if distance > 0:
                direction_x = distance_x / distance
                direction_y = distance_y / distance

                # Apply the velocity to the stone's position
                stone_rect.x += direction_x * self.stone_move_velocity
                stone_rect.y += direction_y * self.stone_move_velocity

                # Decelerate when closer to the mouse
                if abs(distance_x) < self.stone_move_velocity:
                    stone_rect.x = mouse_pos[0] - stone_rect.width / 2
                if abs(distance_y) < self.stone_move_velocity:
                    stone_rect.y = mouse_pos[1] - stone_rect.height / 2

                # Ensure the stone can pass by the mouse
                if distance < self.stone_move_acceleration:
                    self.stone_move_velocity *= -1  # Invert the velocity to pass by the mouse

    def releasing_stone(self):
        if not self.selected_stone:
            return
        self.falling_stone, self.selected_stone = self.selected_stone, None

    def stone_fall(self, mortar):
        if not self.falling_stone:
            return
        if self.stone_fall_velocity <= self.fall_acceleration:
            self.stone_fall_velocity += self.fall_acceleration_increment * self.fall_acceleration_multiplier
        self.falling_stone.rect.y += self.stone_fall_velocity
        self.stone_reset(mortar)

    def stone_reset(self, mortar):
        if self.falling_stone.rect.y > mortar.rect.y:
            mortar.ingredients.append(self.falling_stone)
            print(f"Total ingredients: {mortar.ingredients}")
            self.falling_stone.rect.x = self.falling_stone.x
            self.falling_stone.rect.y = self.falling_stone.y
            self.falling_stone = None
            self.stone_fall_velocity = 0
            return
        if self.falling_stone.rect.y > constants.WINDOW_HEIGHT:
            self.falling_stone.rect.x = self.falling_stone.x
            self.falling_stone.rect.y = self.falling_stone.y
            self.falling_stone = None
            self.stone_fall_velocity = 0

    @staticmethod
    def get_mouse_speed(event_rel):
        dx, dy = event_rel
        speed = (dx ** 2 + dy ** 2) ** (1 / 2)  # Pythagorean formula
        print(f"Mouse speed: {speed}, dx: {dx}, dy: {dy}")
        return speed


class Mortar:
    def __init__(self):
        self.width = 400
        self.height = 50
        self.x = (constants.WINDOW_WIDTH - self.width) / 2
        self.y = (constants.WINDOW_HEIGHT - self.height) / 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ingredients = []

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect)
