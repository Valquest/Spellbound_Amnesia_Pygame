import pygame

from data import entities
from variables import constants


class MagicStone:
    def __init__(self, stone_type, rarity, image_path, x_pos, y_pos, radius, player_inv_instance):
        # CORE VARIABLES
        self.player_inv_instance = player_inv_instance

        # stone variables
        self.stone_type = stone_type
        self.rarity = rarity
        self.image_path = image_path
        self.ammount = self.player_inv_instance.inventory[self.stone_type]

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

        # Movement and rotation variables
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation_angle_velocity = 0
        self.angle = 0

        # Position where the stone was picked up
        self.pickup_position = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def reset_position_and_rotation(self):
        self.center = self.pickup_position
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation_angle_velocity = 0
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.center)

    def update_inv_ammount(self):
        self.ammount = self.player_inv_instance.inventory[self.stone_type]
        self.font_render = self.stone_ammount_font.render(f"{self.ammount}X", True, (0, 0, 0))


class StoneInventory:
    def __init__(self, player_inv_instance):
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

        # player inventory instance
        self.player_inv_instance = player_inv_instance

        for index, (stone_name, stone_attributes) in enumerate(entities.stone_types.items()):
            stone = MagicStone(stone_name, stone_attributes["rarity"], stone_attributes["image_path"],
                               self.x + self.width / 2, self.y + 40 + (60 * index), 20, self.player_inv_instance)
            for stone_type, amount in entities.player_inv.items():
                if stone_name == stone_type:
                    stone.ammount = amount
                    break
            self.magic_stones.append(stone)

        # stone movement variables
        self.selected_stones = []
        self.falling_stones = []
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
        if self.falling_stones or self.selected_stones:
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
        if self.falling_stones or self.selected_stones:
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
        if self.falling_stones or self.selected_stones:
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
        Assigns a stone to the selected_stones list when the player selects a stone with the mouse.
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        selection_radius_multiplier = 1.5  # Adjust this value to increase the selection area

        for stone in self.magic_stones:
            distance = pygame.math.Vector2(mouse_pos).distance_to(pygame.math.Vector2(stone.center))
            if distance <= stone.radius * selection_radius_multiplier and stone not in self.selected_stones:
                stone.pickup_position = stone.center  # Record the pickup position
                self.selected_stones.append(stone)
                break
        self.scroll_velocity = 0

    def move_stone(self) -> None:
        for stone in self.selected_stones:
            mouse_pos = pygame.mouse.get_pos()
            stone_center = stone.center

            offset = stone.radius // self.offset
            pivot_point = pygame.math.Vector2(stone_center[0], stone_center[1] - offset)
            direction = pygame.math.Vector2(mouse_pos) - pivot_point
            distance = direction.length()

            if distance > 0:
                direction = direction.normalize()

            max_acceleration = 0.06 * distance
            acceleration = direction * min(self.stone_move_acceleration_increment * distance, max_acceleration)
            stone.velocity += acceleration
            stone.velocity *= self.damping_factor

            stone_center = (stone_center[0] + stone.velocity.x, stone_center[1] + stone.velocity.y)
            stone.center = stone_center

            stop_threshold = 5
            if distance < stop_threshold:
                stone.velocity *= 0.5
                if stone.velocity.length() < 0.1:
                    stone.velocity = pygame.math.Vector2(0, 0)
                    stone_center = (mouse_pos[0], mouse_pos[1] + offset)
                    stone.center = stone_center

            self.rotate_stone(stone, mouse_pos)

    @staticmethod
    def rotate_stone(stone, mouse_pos) -> None:
        stone_center = stone.center
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(stone_center)
        angular_force = direction.length() * 0.035

        if direction.x < 0:
            stone.rotation_angle_velocity += angular_force
        else:
            stone.rotation_angle_velocity -= angular_force

        stone.rotation_angle_velocity *= 0.92
        stone.angle += stone.rotation_angle_velocity
        stone.rotation_angle_velocity -= stone.angle * 0.05

        stone.image = pygame.transform.rotate(stone.original_image, stone.angle)
        new_rect = stone.image.get_rect(center=stone_center)
        stone.rect = new_rect
        stone.rect.center = stone_center

    def releasing_stone(self):
        if not self.selected_stones:
            return
        for stone in self.selected_stones:
            self.falling_stones.append((stone, stone.velocity, stone.rotation_angle_velocity))
        self.selected_stones.clear()

    def stone_fall(self, mortar):
        for stone, velocity, rotation_velocity in self.falling_stones:
            gravity = pygame.math.Vector2(0, 0.5)
            velocity += gravity

            stone.center = (stone.center[0] + velocity.x, stone.center[1] + velocity.y)
            stone.rect.center = stone.center

            stone.angle += rotation_velocity
            rotation_velocity *= 0.98

            stone.image = pygame.transform.rotate(stone.original_image, stone.angle)
            new_rect = stone.image.get_rect(center=stone.center)
            stone.rect = new_rect

        self.falling_stones = [(stone, velocity, rotation_velocity) for stone, velocity, rotation_velocity in
                               self.falling_stones if not self.stone_reset(stone, mortar)]

    @staticmethod
    def stone_reset(stone, mortar):
        if (mortar.rect.x < stone.center[0] < mortar.rect.x + mortar.width and
                stone.center[1] - stone.radius > mortar.rect.y):
            mortar.ingredients.append(stone)
            stone.player_inv_instance.remove_stone(stone)
            print(f"Total ingredients: {mortar.ingredients}")
            stone.reset_position_and_rotation()
            return True
        if stone.center[1] - stone.radius > constants.WINDOW_HEIGHT:
            stone.reset_position_and_rotation()
            return True
        return False

    @staticmethod
    def get_mouse_speed(event_rel):
        dx, dy = event_rel
        speed = (dx ** 2 + dy ** 2) ** (1 / 2)  # Pythagorean formula
        return speed


class Mortar:
    def __init__(self):
        # CORE VARIABLES
        # mortar variables
        self.mortar_width = 400
        self.mortar_height = 50
        self.mortar_x = (constants.WINDOW_WIDTH - self.mortar_width) / 2
        self.mortar_y = (constants.WINDOW_HEIGHT - self.mortar_height) / 2
        self.mortar_rect = pygame.Rect(self.mortar_x, self.mortar_y, self.mortar_width, self.mortar_height)
        self.ingredients = []

        # spinner dial
        self.dial_width = 100
        self.dial_height = 100
        self.dial_angle = 0
        self.spinning = False
        self.last_mouse_angle = 0
        self.dial_rect = pygame.Rect(self.mortar_rect.centerx - self.dial_width / 2, self.mortar_rect.centery +
                                     100, self.dial_width, self.dial_height)

    def draw(self, screen):
        self.draw_mortar(screen)
        self.draw_dial(screen)

    def draw_mortar(self, screen):
        pygame.draw.rect(screen, "white", self.mortar_rect)

    def draw_dial(self, screen):
        pygame.draw.rect(screen, "gray", self.dial_rect)

    def spin_dial(self, event):
        import math
        self.spinning = True
        # Calculate initial angle
        mouse_x, mouse_y = event.pos
        rel_x, rel_y = mouse_x - self.dial_rect.centerx, mouse_y - self.dial_rect.centery
        self.last_mouse_angle = math.atan2(rel_y, rel_x)

    def update_dial_angle(self):
        import math
        if self.spinning:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.dial_rect.centerx, mouse_y - self.dial_rect.centery
            current_mouse_angle = math.atan2(rel_y, rel_x)

            # Calculate the angle difference
            angle_diff = math.degrees(current_mouse_angle - self.last_mouse_angle)
            self.dial_angle += angle_diff
            last_mouse_angle = current_mouse_angle

        # rotated_dial_image = pygame.transform.rotate(self.dial_image, -self.dial_angle)  # for future implementation
        # rotated_dial_rect = rotated_dial_image.get_rect(center=self.dial_rect.center)


class PlayerInventory:
    def __init__(self):
        self.inv_file_path = r"./data/player_inv.json"
        self.inventory = self.load_player_inventory()
        self.spellcraft_instance = None

    def load_player_inventory(self):
        import json
        with open(self.inv_file_path, 'r') as file:
            return json.load(file)

    def save_player_inventory(self, inventory):
        import json
        with open(self.inv_file_path, 'w') as file:
            json.dump(inventory, file, indent=4)

    def add_stone(self, stone_type, stone):
        self.inventory[stone_type] += 1
        self.save_player_inventory(self.inventory)
        stone.update_inv_ammount()

    def remove_stone(self, stone):
        if stone.ammount > 0:
            self.inventory[stone.stone_type] -= 1
            self.save_player_inventory(self.inventory)
            stone.update_inv_ammount()
