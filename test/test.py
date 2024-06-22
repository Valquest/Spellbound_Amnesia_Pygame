import pygame
import sys

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
large_rect = pygame.Rect(300, 150, 200, 300)

# Smaller rectangles
rect_width, rect_height = 180, 50
num_rects = 10
rects = [pygame.Rect(310, 160 + i * (rect_height + 10), rect_width, rect_height) for i in range(num_rects)]

# Scroll variables
scroll_y = 0
scroll_speed = 10

# Fade area
fade_height = 20


def draw_fading_rects(surface, rects, scroll_y, large_rect, fade_height):
    for rect in rects:
        new_rect = rect.move(0, scroll_y)

        # Calculate intersection with large rectangle
        if new_rect.bottom < large_rect.top or new_rect.top > large_rect.bottom:
            continue

        temp_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        temp_surface.fill(GRAY)

        # Apply gradient fading effect at the top
        if new_rect.top < large_rect.top + fade_height:
            for i in range(fade_height):
                alpha = max(0, 255 - int((large_rect.top + fade_height - new_rect.top - i) / fade_height * 255))
                pygame.draw.line(temp_surface, (200, 200, 200, alpha), (0, i), (rect_width, i))

        # Apply gradient fading effect at the bottom
        if new_rect.bottom > large_rect.bottom - fade_height:
            for i in range(fade_height):
                alpha = max(0, 255 - int((new_rect.bottom - large_rect.bottom + fade_height - i) / fade_height * 255))
                pygame.draw.line(temp_surface, (200, 200, 200, alpha), (0, rect_height - i - 1),
                                 (rect_width, rect_height - i - 1))

        # Clip the temporary surface to the part within the large rectangle
        clip_rect = new_rect.clip(large_rect)
        clip_temp_surface = temp_surface.subsurface(
            clip_rect.left - new_rect.left,
            clip_rect.top - new_rect.top,
            clip_rect.width,
            clip_rect.height
        )
        surface.blit(clip_temp_surface, clip_rect.topleft)


clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y += scroll_speed
            elif event.button == 5:  # Scroll down
                scroll_y -= scroll_speed

    screen.fill(WHITE)

    # Draw large rectangle
    pygame.draw.rect(screen, BLACK, large_rect, 2)

    # Draw fading rectangles
    draw_fading_rects(screen, rects, scroll_y, large_rect, fade_height)

    pygame.display.flip()
    clock.tick(30)
