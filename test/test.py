import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scrolling Rectangles with Fading')

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Large rectangle dimensions
display_rect = pygame.Rect(300, 150, 200, 300)

# Smaller rectangles
rect_width, rect_height = 180, 50
num_rects = 10
rects = [pygame.Rect(310, 160 + i * (rect_height + 10), rect_width, rect_height) for i in range(num_rects)]

clock = pygame.time.Clock()
running = True











# Scroll settings
scroll_speed = 5
scroll_velocity = 0
deceleration = 0.94
min_velocity = 0.1
tiny_increment_threshold = min_velocity
tiny_increment_deceleration = 0.999

# Bounce settings
bounce_active = False
bounce_amplitudes = [10, -10, 5, -5, 2, -2]
current_bounce_index = 0
bounce_velocity = 0
bounce_damping = 0.9


# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_velocity += event.y * scroll_speed
            bounce_active = True  # Reset bounce active on new scroll
            current_bounce_index = 0  # Reset bounce oscillation index
            bounce_velocity = 0  # Reset bounce velocity on new scroll

    # Apply scroll velocity
    if abs(scroll_velocity) > min_velocity:
        for rect in rects:
            rect.y += scroll_velocity

        # Use a less aggressive deceleration for tiny increments
        if abs(scroll_velocity) < tiny_increment_threshold:
            scroll_velocity *= tiny_increment_deceleration
        else:
            scroll_velocity *= deceleration

    # Apply bounce effect
    if bounce_active and scroll_velocity < min_velocity:
        for rect in rects:
            rect.y += bounce_velocity

        # Apply damping to slow down as it approaches the peak of the bounce
        bounce_velocity *= bounce_damping

        # Check if bounce should change direction
        if abs(bounce_velocity) < min_velocity:
            current_bounce_index += 1
            if current_bounce_index < len(bounce_amplitudes):
                bounce_velocity = -bounce_amplitudes[current_bounce_index]
            else:
                bounce_velocity = 0
                bounce_active = False












    screen.fill(WHITE)

    # Draw large rectangle
    pygame.draw.rect(screen, BLACK, display_rect, 2)

    # Draw only the parts of the rectangles that are within the display rectangle
    for rect in rects:
        intersection_rect = display_rect.clip(rect)

        if intersection_rect.width > 0 and intersection_rect.height > 0:
            # Create a new surface to hold the visible part of the rectangle
            result_surface = pygame.Surface((intersection_rect.width, intersection_rect.height))
            result_surface.fill(BLACK)

            # Blit the part of the rectangle that is within the intersection rectangle
            screen.blit(result_surface, intersection_rect.topleft)

    pygame.display.flip()
    clock.tick(60)
