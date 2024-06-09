from . import constants as c
from utils.classes import Card

lane_start_x = c.LANE_STARTING_X
lane_start_y = c.LANE_STARTING_Y / 6
lane_height = c.LANE_HEIGHT_CONST / 6
col_width = (c.WINDOW_WIDTH - c.LANE_STARTING_X - c.MARGIN) / c.COL_NUMBER + 4
amnesia_bar_x = (Card.card_width + c.MARGIN) * c.CARD_COUNT + 100
amnesia_bar_y = 5 * c.MARGIN
