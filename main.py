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
CARD_COUNT = 5

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
cards = []
card_types = {
    "damage1": 1,
    "freeze2": 2,
    "damage2": 2
}
rand_numb_of_enemies = random.randint(1, 4)
font = pygame.font.SysFont(None, 32)

# creating enemy position matrix for coordinates and slot availability
enemy_position_matrix = []

for row in range(ROW_NUMBER):
    row_position = []
    for col in range(COL_NUMBER):
        x_pos = int(round((WIDTH - MARGIN - ((COL_WIDTH - border_thickness) * col) - COL_WIDTH / 2), 0))
        y_pos = int(round((HEIGHT - MARGIN - (LANE_HEIGHT * (3 - row)) + LANE_HEIGHT / 2), 0))
        occupied = False
        position = [x_pos, y_pos, occupied]
        row_position.append(position)
    enemy_position_matrix.append(row_position)

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


def enemy_finder(lane):
    last_position = None
    print(lane)
    for index in list(reversed(enemy_position_matrix[lane])):
        if index[2]:
            print(f"col {index} value: {index[2]}")
            last_position = index
            break
    return last_position


#def turn_calculation(card1, lane1, card2, lane2, card3, lane3):


# enemies
class Card:
    card_width = 120
    card_height = 250
    click_color = "dark grey"

    def __init__(self, x_cord, y_cord, color):
        self.x_cord = x_cord + MARGIN
        self.y_cord = MARGIN
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x_cord, self.y_cord, self.card_width, self.card_height))


class Enemy:
    enemy_width = 50
    enemy_height = 50
    position = []
    health = 1

    def __init__(self, lane_pos, col_pos, color):
        self.lane_pos = lane_pos
        self.col_pos = col_pos
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.col_pos, self.lane_pos, self.enemy_width, self.enemy_height))


# generate enemies

for _ in range(rand_numb_of_enemies):
    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    random_row = random.randint(0, len(enemy_position_matrix) - 1)

    for index, col in enumerate(enemy_position_matrix[random_row]):
        if not col[2]:
            enemy = Enemy(enemy_position_matrix[random_row][index][1] - Enemy.enemy_width / 2,
                          enemy_position_matrix[random_row][index][0] - Enemy.enemy_height / 2, random_color)
            enemy_position_matrix[random_row][index][2] = True
            enemy.position = enemy_position_matrix[random_row][index]
            enemies.append(enemy)
            break

for i, enemy in enumerate(enemies):
    print(f"enemy {i} : {enemy.position}")

# this code draws all enemies in all possible positions
'''
for row in range(ROW_NUMBER):
    for col in range(COL_NUMBER):
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        enemy = Enemy(enemy_position_matrix[row][col][1] - Enemy.enemy_width / 2,
                      enemy_position_matrix[row][col][0] - Enemy.enemy_height / 2, random_color)
        enemies.append(enemy)
'''

# generating game cards
for count in range(CARD_COUNT):
    random_card = random.randint(0, len(card_types) - 1)
    temp_card = Card(150 * count + 1, 0, "gray")
    cards.append(temp_card)

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
                    print(selected_lane)

                    # kill enemy when lane is selected
                    enemy_to_kill_position = enemy_finder(lanes.index(lane))
                    for enemy in enemies:
                        if enemy.position == enemy_to_kill_position:
                            enemy.health -= 1

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

    # updates enemy list
    enemies = [enemy for enemy in enemies if enemy.health > 0]

    # drawing enemies
    for enemy in enemies:
        enemy.draw(screen)

    # drawing cards
    for card in cards:
        card.draw(screen)

    # rendering game here

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
