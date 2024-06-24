import pygame

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
min_velocity = 0.01
tiny_increment_threshold = min_velocity
tiny_increment_deceleration = 0.999

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_velocity += event.y * scroll_speed

        # Apply scroll velocity
        if abs(scroll_velocity) > min_velocity:
            # Check the position of the topmost and bottommost rectangles
            topmost_rect = rects[0]
            bottommost_rect = rects[-1]

            # If scrolling up, ensure the topmost rectangle does not go above the top of the large rectangle
            if scroll_velocity > 0 and topmost_rect.top + scroll_velocity >= display_rect.top:
                scroll_velocity = (display_rect.top - topmost_rect.top) if topmost_rect.top < display_rect.top else 0

            # If scrolling down, ensure the bottommost rectangle does not go below the bottom of the large rectangle
            elif scroll_velocity < 0 and bottommost_rect.bottom + scroll_velocity <= display_rect.bottom:
                scroll_velocity = (
                            display_rect.bottom - bottommost_rect.bottom) if bottommost_rect.bottom > display_rect.bottom else 0

            for rect in rects:
                rect.y += scroll_velocity

            # Use a less aggressive deceleration for tiny increments
            if abs(scroll_velocity) < tiny_increment_threshold:
                scroll_velocity *= tiny_increment_deceleration
            else:
                scroll_velocity *= deceleration

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