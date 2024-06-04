import pygame

# constant variables
WIDTH = 1280
HEIGHT = 720
LANE_START = 280
LANE_HEIGHT = HEIGHT/6 - 10

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption('Spellbound Amnesia')

# variables
border_thickness = 5
lane_color = (0, 0, 0) # black
selected_lane_color = (255, 0 ,0) # red
selected_lane = None # stores info on which lane is selected

# objects
# lanes
lanes = [
    pygame.Rect(LANE_START, HEIGHT/6*3, WIDTH - LANE_START - 10, LANE_HEIGHT),
    pygame.Rect(LANE_START, HEIGHT/6*4, WIDTH - LANE_START - 10, LANE_HEIGHT),
    pygame.Rect(LANE_START, HEIGHT/6*5, WIDTH - LANE_START - 10, LANE_HEIGHT)
]

# enemies


while running:
    # poll for events
    # pygame.Quit event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # check if clicked inside any rectangle
            for lane in lanes:
                if lane.collidepoint(mouse_pos):
                    selected_lane = lanes.index(lane)
                    break # exits loop if condition is met

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((102, 140, 255))

    # drawing lanes

    for i, lane in enumerate(lanes):
        if i == selected_lane and selected_lane is not None:
            pygame.draw.rect(screen, selected_lane_color, lane, border_thickness)
        else:
            pygame.draw.rect(screen, lane_color, lane, border_thickness)


    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()