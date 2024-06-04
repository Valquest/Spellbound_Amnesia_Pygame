import pygame

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
LANE_START = 280
LANE_HEIGHT = HEIGHT/6 - 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption('Spellbound Amnesia')

# objects
border_thickness = 5
lane1 = pygame.Rect(LANE_START, HEIGHT/6*3, WIDTH - LANE_START - 10, LANE_HEIGHT)
lane2 = pygame.Rect(LANE_START, HEIGHT/6*4, WIDTH - LANE_START - 10, LANE_HEIGHT)
lane3 = pygame.Rect(LANE_START, HEIGHT/6*5, WIDTH - LANE_START - 10, LANE_HEIGHT)

while running:
    # poll for events
    # pygame.Quit event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((102, 140, 255))

    # drawing lanes
    pygame.draw.rect(screen, (0, 0, 0), lane1, border_thickness)
    pygame.draw.rect(screen, (0, 0, 0), lane2, border_thickness)
    pygame.draw.rect(screen, (0, 0, 0), lane3, border_thickness)


    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()