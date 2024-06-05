import pygame
import random
# project files
from utils import classes
from variables import constants
from core import core_funct
from utils import util_funct
from data import entities


def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    pygame.display.set_caption('Spellbound Amnesia')

    # variables
    selected_lane_color = (255, 0, 0)
    border_thickness = 5
    selected_lane = None
    enemies = []
    cards = []

    rand_numb_of_enemies = random.randint(4, 8)

    # creating enemy position matrix for coordinates and slot availability
    enemy_position_matrix = []

    for row in range(constants.ROW_NUMBER):
        row_position = []
        for col in range(constants.COL_NUMBER):
            x_pos = int(round((constants.WINDOW_WIDTH - constants.MARGIN -
                               ((constants.COL_WIDTH - border_thickness) * col) - constants.COL_WIDTH / 2), 0))
            y_pos = int(round((constants.WINDOW_HEIGHT - constants.MARGIN - (constants.LANE_HEIGHT * (3 - row)) +
                               constants.LANE_HEIGHT / 2), 0))
            occupied = False
            position = [x_pos, y_pos, occupied]
            row_position.append(position)
        enemy_position_matrix.append(row_position)

    # create lanes
    lanes = util_funct.add_lanes(constants.ROW_NUMBER)

    # def turn_calculation(card1, lane1, card2, lane2, card3, lane3):

    # generate enemies
    for _ in range(rand_numb_of_enemies):
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        random_row = random.randint(0, len(enemy_position_matrix) - 1)

        for index, col in enumerate(enemy_position_matrix[random_row]):
            if not col[2]:
                enemy = classes.Enemy(enemy_position_matrix[random_row][index][1] - classes.Enemy.enemy_width / 2,
                                      enemy_position_matrix[random_row][index][0] - classes.Enemy.enemy_height / 2,
                                      random_color)
                enemy_position_matrix[random_row][index][2] = True
                enemy.position = enemy_position_matrix[random_row][index]
                enemies.append(enemy)
                break

    # this code draws all enemies in all possible positions
    '''
    for row in range(constants.ROW_NUMBER):
        for col in range(constants.COL_NUMBER):
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            enemy = Enemy(enemy_position_matrix[row][col][1] - Enemy.enemy_width / 2,
                          enemy_position_matrix[row][col][0] - Enemy.enemy_height / 2, random_color)
            enemies.append(enemy)
    '''

    # generating game cards
    for count in range(constants.CARD_COUNT):
        random_card_type = random.choice(list(entities.card_types.keys()))
        temp_card = classes.Card(150 * count + 1, 0, "gray")
        temp_card.type = entities.card_types[random_card_type]
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

                        # kill enemy when lane is selected
                        enemy_to_kill_position = core_funct.enemy_finder(lanes.index(lane), enemy_position_matrix)
                        for enemy in enemies:
                            if enemy.position == enemy_to_kill_position:
                                enemy.health -= 1

                        # exits loop if condition is met
                        break

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((102, 140, 255))

        # draw columns/spots
        spots = util_funct.add_columns(constants.COL_NUMBER)
        for col in spots:
            pygame.draw.rect(screen, "black", col, border_thickness)

        # drawing lanes
        for i, lane in enumerate(lanes):
            if i == selected_lane and selected_lane is not None:
                pygame.draw.rect(screen, selected_lane_color, lane, border_thickness)
            else:
                pygame.draw.rect(screen, "black", lane, border_thickness)

        # updates enemy list and matrix
        for enemy in enemies[:]:
            if enemy.health <= 0:
                enemies.remove(enemy)
                for index, position in enumerate(enemy_position_matrix[selected_lane]):
                    if enemy.position == position:
                        enemy_position_matrix[selected_lane][index][2] = False

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


if __name__ == "__main__":
    main()
