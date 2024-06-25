import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scrolling Rectangles with Fading')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Large rectangle dimensions
display_rect = pygame.Rect(300, 150, 200, 300)

# Padding for the spring back boundary
padding = 10

# Smaller rectangles
rect_width, rect_height = 180, 50
num_rects = 8
rects = [pygame.Rect(310, 160 + i * (rect_height + 10), rect_width, rect_height) for i in range(num_rects)]

clock = pygame.time.Clock()
running = True

# Scroll settings
scroll_speed = 5
scroll_velocity = 0
deceleration = 0.94
min_velocity = 0.01
tiny_increment_threshold = min_velocity
tiny_increment_deceleration = 0.999
max_scroll_offset = 100

# Hard scroll limits
scroll_limit_distance = 70
top_hard_limit = display_rect.top + scroll_limit_distance
bottom_hard_limit = display_rect.bottom - scroll_limit_distance

# Spring back settings
spring_back_active = False
spring_back_speed = 2
target_offset = 0

# Function to calculate resistance based on proximity to limits
def calculate_resistance(position, limit, max_offset):
    offset = abs(position - limit)
    if offset > max_offset:
        offset = max_offset
    resistance = (max_offset - offset) / max_offset
    return resistance

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_velocity += event.y * scroll_speed
            spring_back_active = False  # Reset spring back active on new scroll

    # Apply scroll velocity
    if abs(scroll_velocity) > min_velocity:
        for rect in rects:
            rect.y += scroll_velocity

        # Deceleration
        if abs(scroll_velocity) < tiny_increment_threshold:
            scroll_velocity *= tiny_increment_deceleration
        else:
            scroll_velocity *= deceleration

        # Hard boundary enforcement during scrolling
        if rects[0].top > top_hard_limit:
            for rect in rects:
                rect.y = max(rect.y - scroll_velocity, top_hard_limit + rects.index(rect) * (rect_height + 10))
            scroll_velocity = 0
        elif rects[-1].bottom < bottom_hard_limit:
            for rect in rects:
                rect.y = min(rect.y - scroll_velocity, bottom_hard_limit - (num_rects - rects.index(rect)) * (rect_height + 10))
            scroll_velocity = 0

        # Increase resistance the further you scroll past the limit
        if rects[0].top > display_rect.top + padding:
            resistance = calculate_resistance(rects[0].top, display_rect.top + padding, max_scroll_offset)
            scroll_velocity *= resistance
        elif rects[-1].bottom < display_rect.bottom - padding:
            resistance = calculate_resistance(rects[-1].bottom, display_rect.bottom - padding, max_scroll_offset)
            scroll_velocity *= resistance

    else:
        scroll_velocity = 0

    # Check for spring back activation
    if not spring_back_active:
        if rects[0].top > display_rect.top + padding:
            target_offset = (display_rect.top + padding) - rects[0].top
            spring_back_active = True
        elif rects[-1].bottom < display_rect.bottom - padding:
            target_offset = (display_rect.bottom - padding) - rects[-1].bottom
            spring_back_active = True

    # Apply spring back
    if spring_back_active:
        spring_back_factor = 1 + abs(target_offset) / max_scroll_offset
        if target_offset > 0:
            resistance = calculate_resistance(rects[-1].bottom, display_rect.bottom - padding, max_scroll_offset)
            for rect in rects:
                rect.y += spring_back_speed * spring_back_factor * resistance
            if rects[-1].bottom >= display_rect.bottom - padding:
                offset = rects[-1].bottom - (display_rect.bottom - padding)
                for rect in rects:
                    rect.y -= offset
                spring_back_active = False
        elif target_offset < 0:
            resistance = calculate_resistance(rects[0].top, display_rect.top + padding, max_scroll_offset)
            for rect in rects:
                rect.y -= spring_back_speed * spring_back_factor * resistance
            if rects[0].top <= display_rect.top + padding:
                offset = (display_rect.top + padding) - rects[0].top
                for rect in rects:
                    rect.y += offset
                spring_back_active = False

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

pygame.quit()
