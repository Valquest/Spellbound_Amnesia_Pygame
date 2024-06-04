import pygame
import random

# constant variables
COL_NUMBER = 8
ROW_NUMBER = 3
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

selected_lane_color = (255, 0, 0)
border_thickness = 5

# stores info on which lane is selected
selected_lane = None
enemies = []

rand_numb_of_enemies = random.randint(1, 4)
random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# creating enemy position matrix for coordinates and slot availability
enemy_position_matrix = []

for row in range(ROW_NUMBER):
    for col in range(COL_NUMBER):
        x_pos = (WIDTH - MARGIN - (COL_WIDTH * col) - COL_WIDTH / 2)
        y_pos = (HEIGHT - MARGIN - (LANE_HEIGHT * (3 - row)) + LANE_HEIGHT / 2)
        occupied = False
        position = (x_pos, y_pos, occupied)
        enemy_position_matrix.append(position)

print(enemy_position_matrix)

# objects
# lanes
lanes = [
    pygame.Rect(LANE_START_X, LANE_START_Y * 3 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y * 4 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT),
    pygame.Rect(LANE_START_X, LANE_START_Y * 5 - MARGIN, WIDTH - LANE_START_X - MARGIN, LANE_HEIGHT)
]

# columns


def add_columns(number_of_cols):
    cols = []
    for spot in range(number_of_cols):
        column = pygame.Rect(COL_START + ((COL_WIDTH - 5) * spot + 1), LANE_START_Y * 3 - MARGIN,
                             COL_WIDTH, HEIGHT - LANE_START_Y * 3)
        cols.append(column)
    return cols


# enemies
class Enemy:
    def __init__(self, lane_pos, col_pos):
        self.lane_pos = lane_pos
        self.col_pos = ((WIDTH - LANE_START_X - MARGIN) / COL_NUMBER + 4) * COL_NUMBER - col_pos

    def draw(self, canvas):
        pygame.draw.rect(canvas, random_color, (self.col_pos, self.lane_pos, 50, 50))


# generate enemies
for _ in range(rand_numb_of_enemies):
    enemy = Enemy(random.randint(1, 3), random.randint(1, 8))
    enemies.append(enemy)

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
                    # exits loop if condition is met
                    break

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

    # drawing enemies
    for enemy in enemies:
        enemy.draw(screen)

    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
