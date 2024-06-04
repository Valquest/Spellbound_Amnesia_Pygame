import pygame
import random

# constant variables
COL_NUMBER = 8
WIDTH = 1280
HEIGHT = 720
MARGIN = 20
LANE_START_X = 480 + MARGIN
LANE_START_Y = HEIGHT/6
LANE_HEIGHT = HEIGHT/6
COL_START = LANE_START_X
COL_WIDTH = (WIDTH - LANE_START_X - MARGIN) / COL_NUMBER + 4

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

# objects
# lanes
lanes = [
    pygame.Rect(LANE_START_X, LANE_START_Y * 3 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y * 4 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y * 5 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT)
]

# columns
def add_columns(number_of_cols):
    spots = []
    for spot in range(number_of_cols):
        col = pygame.Rect(COL_START + ((COL_WIDTH - 5) * spot + 1), LANE_START_Y * 3 - MARGIN, COL_WIDTH, HEIGHT - LANE_START_Y * 3)
        spots.append(col)
    return spots

# enemies
class enemy():
    def __init__(self, lane_pos, col_pos, color):
        self.color = color
        self.lane_pos = lane_pos
        self.col_pos = ((WIDTH - LANE_START_X - MARGIN) / COL_NUMBER + 4) * COL_NUMBER - col_pos


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

    # draw columns/spots
    spots = add_columns(COL_NUMBER)
    for col in spots:
        pygame.draw.rect(screen, "black", col, border_thickness)

    # drawing lanes
    for i, lane in enumerate(lanes):
        if i == selected_lane and selected_lane is not None:
            pygame.draw.rect(screen, selected_lane_color, lane, border_thickness)
        else:
            pygame.draw.rect(screen, "black", lane, border_thickness)


    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()