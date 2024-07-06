import pygame

from data import entities
from variables import constants


class MagicStone:
    def __init__(self, stone_type, rarity, image_path, x_pos, y_pos, radius):
        # CORE VARIABLES
        # stone variables
        self.stone_type = stone_type
        self.rarity = rarity
        self.image_path = image_path
        self.ammount = 0

        # Circle variables
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.center = (self.x, self.y)
        self.rect_color = "White"
        self.scroll_y_pos = 0

        # Load the image for this specific stone
        original_image = pygame.transform.scale(pygame.image.load(self.image_path), (2 * self.radius, 2 * self.radius))
        self.original_image = original_image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.center)

        # inv ammount of stones variables
        self.stone_ammount_font = pygame.font.Font(None, 32)
        self.font_render = self.stone_ammount_font.render(f"{self.ammount}X", True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class StoneInventory:
    def __init__(self):
        # CORE VARIABLES
        # rect variables
        self.x = 50
        self.y = 100
        self.width = constants.INVENTORY_WIDTH
        self.height = constants.INVENTORY_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.font.init()

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
            stone = MagicStone(stone_name, stone_attributes["rarity"], stone_attributes["image_path"],
                               self.x + self.width / 2, self.y + 40 + (60 * index), 20)
            for stone_type, amount in entities.player_inv.items():
                if stone_name == stone_type:
                    stone.ammount = amount
                    break
            self.magic_stones.append(stone)

        # stone movement variables
        self.selected_stone = None
        self.falling_stone = None
        self.mouse_speed = 0
        self.stone_move_velocity = pygame.math.Vector2(0, 0)
        self.stone_move_acceleration = 10
        self.stone_move_acceleration_increment = 0.2
        self.stone_move_acceleration_multiplier = 0.90
        self.damping_factor = 0.78  # Damping factor to simulate deceleration
        self.angle = 0
        self.rotation_angle_velocity = 0
        self.offset = 1.85

        # stone fall movement variables
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
        if (self.scroll_velocity > 0 and self.magic_stones[0].center[1] - self.magic_stones[
            0].radius >= self.top_hard_limit) or \
                (self.scroll_velocity < 0 and self.magic_stones[-1].center[1] + self.magic_stones[
                    -1].radius <= self.bottom_hard_limit):
            self.scroll_velocity = 0

        if abs(self.scroll_velocity) > self.min_velocity:
            for stone in self.magic_stones:
                stone.center = (stone.center[0], stone.center[1] + self.scroll_velocity)

            # Deceleration
            if abs(self.scroll_velocity) < self.tiny_increment_threshold:
                self.scroll_velocity *= self.tiny_increment_deceleration
            else:
                self.scroll_velocity *= self.deceleration

            # Hard boundary enforcement during scrolling
            if self.magic_stones[0].center[1] - self.magic_stones[0].radius > self.top_hard_limit:
                for stone in self.magic_stones:
                    stone.center = (stone.center[0], max(
                        stone.center[1] - self.scroll_velocity,
                        self.top_hard_limit + self.magic_stones.index(stone) * (2 * stone.radius + 10)
                    ))
                self.scroll_velocity = 0
            elif self.magic_stones[-1].center[1] + self.magic_stones[-1].radius < self.bottom_hard_limit:
                for stone in self.magic_stones:
                    stone.center = (stone.center[0], min(
                        stone.center[1] - self.scroll_velocity,
                        self.bottom_hard_limit - (
                                len(self.magic_stones) - self.magic_stones.index(stone)) * (2 * stone.radius + 10)
                    ))
                self.scroll_velocity = 0

            # Increase resistance the further you scroll past the limit
            if self.magic_stones[0].center[1] - self.magic_stones[0].radius > self.rect.top + self.padding:
                resistance = self.calculate_resistance(
                    self.magic_stones[0].center[1] - self.magic_stones[0].radius,
                    self.rect.top + self.padding,
                    self.max_scroll_offset
                )
                self.scroll_velocity *= resistance
            elif self.magic_stones[-1].center[1] + self.magic_stones[-1].radius < self.rect.bottom - self.padding:
                resistance = self.calculate_resistance(
                    self.magic_stones[-1].center[1] + self.magic_stones[-1].radius,
                    self.rect.bottom - self.padding,
                    self.max_scroll_offset
                )
                self.scroll_velocity *= resistance
        else:
            self.scroll_velocity = 0

    def check_spring_back_activation(self):
        # Check if any items are selected or falling, if yes, exit function
        if self.falling_stone or self.selected_stone:
            return
        if not self.spring_back_active:
            if self.magic_stones[0].center[1] - self.magic_stones[0].radius > self.rect.top + self.padding:
                self.target_offset = (self.rect.top + self.padding) - (
                            self.magic_stones[0].center[1] - self.magic_stones[0].radius)
                self.spring_back_active = True
            elif self.magic_stones[-1].center[1] + self.magic_stones[-1].radius < self.rect.bottom - self.padding:
                self.target_offset = (self.rect.bottom - self.padding) - (
                            self.magic_stones[-1].center[1] + self.magic_stones[-1].radius)
                self.spring_back_active = True

    def apply_spring_back(self):
        # check if any items are selected or falling, if yes, exit function
        if self.falling_stone or self.selected_stone:
            return
        if self.spring_back_active:
            spring_back_factor = 1 + abs(self.target_offset) / self.max_scroll_offset
            if self.target_offset > 0:
                resistance = self.calculate_resistance(
                    self.magic_stones[-1].center[1] + self.magic_stones[-1].radius,
                    self.rect.bottom - self.scroll_limit_distance,
                    self.max_scroll_offset
                )
                for stone in self.magic_stones:
                    stone.center = (stone.center[0], stone.center[1] +
                                    self.spring_back_speed * spring_back_factor * resistance)
                if self.magic_stones[-1].center[1] + self.magic_stones[-1].radius >= self.rect.bottom - self.padding:
                    offset = (self.magic_stones[-1].center[1] + self.magic_stones[-1].radius) - (
                                self.rect.bottom - self.padding)
                    for stone in self.magic_stones:
                        stone.center = (stone.center[0], stone.center[1] - offset)
                    self.spring_back_active = False
            elif self.target_offset < 0:
                resistance = self.calculate_resistance(
                    self.magic_stones[0].center[1] - self.magic_stones[0].radius,
                    self.rect.top + self.scroll_limit_distance,
                    self.max_scroll_offset
                )
                for stone in self.magic_stones:
                    stone.center = (stone.center[0], stone.center[1] -
                                    self.spring_back_speed * spring_back_factor * resistance)
                if self.magic_stones[0].center[1] - self.magic_stones[0].radius <= self.rect.top + self.padding:
                    offset = (self.rect.top + self.padding) - (
                                self.magic_stones[0].center[1] - self.magic_stones[0].radius)
                    for stone in self.magic_stones:
                        stone.center = (stone.center[0], stone.center[1] + offset)
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
        mouse_pos = pygame.mouse.get_pos()
        for stone in self.magic_stones:
            distance = pygame.math.Vector2(mouse_pos).distance_to(pygame.math.Vector2(stone.center))
            if distance <= stone.radius:
                self.selected_stone = stone
                break
        # set scroll velocity to 0 to prevent bug where scrolling happens on item return to inv
        self.scroll_velocity = 0

    def move_stone(self) -> None:
        if self.selected_stone:
            mouse_pos = pygame.mouse.get_pos()
            stone_center = self.selected_stone.center

            # Define the offset above the center
            offset = self.selected_stone.radius // self.offset

            # Calculate the pivot point above the center of the stone
            pivot_point = pygame.math.Vector2(stone_center[0], stone_center[1] - offset)

            # Calculate the direction vector towards the mouse position
            direction = pygame.math.Vector2(mouse_pos) - pivot_point

            # Calculate the distance to the mouse position
            distance = direction.length()

            # Normalize the direction vector
            if distance > 0:
                direction = direction.normalize()

            # Apply acceleration based on the distance with a cap
            max_acceleration = 0.06 * distance  # Adjust this value to control acceleration strength
            acceleration = direction * min(self.stone_move_acceleration_increment * distance, max_acceleration)

            # Update velocity with applied acceleration
            self.stone_move_velocity += acceleration

            # Apply damping to simulate deceleration
            self.stone_move_velocity *= self.damping_factor

            # Apply the velocity to the stone's position
            stone_center = (stone_center[0] + self.stone_move_velocity.x, stone_center[1] + self.stone_move_velocity.y)
            self.selected_stone.center = stone_center

            # Smooth stopping near the mouse position
            stop_threshold = 5  # Increased threshold for smoother stopping

            if distance < stop_threshold:
                self.stone_move_velocity *= 0.5  # Faster deceleration the closer the item is
                if self.stone_move_velocity.length() < 0.1:
                    self.stone_move_velocity = pygame.math.Vector2(0, 0)
                    # Set stone_center directly to mouse_pos adjusted by offset when close enough
                    stone_center = (mouse_pos[0], mouse_pos[1] + offset)
                    self.selected_stone.center = stone_center

            # Call the rotation function with the current mouse position
            self.rotate_stone(mouse_pos)

    def rotate_stone(self, mouse_pos) -> None:
        """
        Rotates the selected stone based on its velocity and mouse movement.
        :param mouse_pos: Current position of the mouse.
        :return: None
        """
        if self.selected_stone:
            stone_center = self.selected_stone.center

            # Calculate the direction of mouse movement
            direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(stone_center)

            # Calculate angular force based on mouse movement
            angular_force = direction.length() * 0.035  # Increase the multiplier for more sensitivity

            # Determine the direction of the applied force
            if direction.x < 0:
                self.rotation_angle_velocity += angular_force
            else:
                self.rotation_angle_velocity -= angular_force

            # Apply stronger damping to simulate friction and ensure stopping
            self.rotation_angle_velocity *= 0.92  # Increase this value for stronger damping

            # Update the angle based on angular velocity
            self.angle += self.rotation_angle_velocity

            # Apply pendulum-like damping to swing back to original position
            self.rotation_angle_velocity -= self.angle * 0.05  # Adjust the damping factor as needed

            # Rotate the stone's image around its center
            self.selected_stone.image = pygame.transform.rotate(self.selected_stone.original_image, self.angle)
            new_rect = self.selected_stone.image.get_rect(center=stone_center)

            # Update the stone's rect based on the new rect position
            self.selected_stone.rect = new_rect

            # Ensure the rect is updated correctly
            self.selected_stone.rect.center = stone_center

    def releasing_stone(self):
        if not self.selected_stone:
            return
        self.falling_stone, self.selected_stone = self.selected_stone, None

    def stone_fall(self, mortar):
        if not self.falling_stone:
            return
        if self.stone_fall_velocity <= self.fall_acceleration:
            self.stone_fall_velocity += self.fall_acceleration_increment * self.fall_acceleration_multiplier
        self.falling_stone.center = (self.falling_stone.center[0],
                                     self.falling_stone.center[1] + self.stone_fall_velocity)
        self.falling_stone.rect.center = self.falling_stone.center
        self.stone_reset(mortar)

    def stone_reset(self, mortar):
        if (mortar.rect.x < self.falling_stone.center[0] < mortar.rect.x + mortar.width and
                self.falling_stone.center[1] - self.falling_stone.radius > mortar.rect.y):
            mortar.ingredients.append(self.falling_stone)
            print(f"Total ingredients: {mortar.ingredients}")
            self.falling_stone.center = (self.falling_stone.x, self.falling_stone.y)
            self.stone_fall_velocity = 0
            self.rotation_angle_velocity = 0
            self.angle = 0
            self.falling_stone.image = pygame.transform.rotate(self.falling_stone.original_image, self.angle)
            self.falling_stone = None
            return
        if self.falling_stone.center[1] - self.falling_stone.radius > constants.WINDOW_HEIGHT:
            self.falling_stone.center = (self.falling_stone.x, self.falling_stone.y)
            self.stone_fall_velocity = 0
            self.rotation_angle_velocity = 0
            self.angle = 0
            self.falling_stone.image = pygame.transform.rotate(self.falling_stone.original_image, self.angle)
            self.falling_stone = None

    @staticmethod
    def get_mouse_speed(event_rel):
        dx, dy = event_rel
        speed = (dx ** 2 + dy ** 2) ** (1 / 2)  # Pythagorean formula
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
