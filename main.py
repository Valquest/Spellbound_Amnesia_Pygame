import pygame

# constant variables
WIDTH = 1280
HEIGHT = 720
LANE_START_X = 280
LANE_START_Y = HEIGHT/6
LANE_HEIGHT = HEIGHT/6
COL_START = LANE_START_X - 2
COL_WIDTH = (WIDTH - LANE_START_X - 10) / 8

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption('Spellbound Amnesia')

# variables

selected_lane_color = (255, 0 ,0) # red
border_thickness = 5
selected_lane = None # stores info on which lane is selected
border_thickness = 5
margin = 10

# objects
# lanes
lanes = [
    pygame.Rect(LANE_START_X, LANE_START_Y*3 - margin, WIDTH - LANE_START_X - margin, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y*4 - margin, WIDTH - LANE_START_X - margin, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y*5 - margin, WIDTH - LANE_START_X - margin, LANE_HEIGHT)
]

# columns
def add_columns(number_of_cols):
    spots = []
    for spot in range(number_of_cols):
        col = pygame.Rect(COL_START + (COL_WIDTH * spot + 1), LANE_START_Y * 3 - margin, COL_WIDTH, HEIGHT - LANE_START_Y - margin)
        spots.append(col)

    return spots

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
            pygame.draw.rect(screen, "black", lane, border_thickness)

    # draw columns/spots
    spots = add_columns(8)
    for col in spots:
        pygame.draw.rect(screen, "black", col, border_thickness)


    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()