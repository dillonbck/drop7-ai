import logging
import pygame
from pygame.locals import *
from gui import Gui


# Log Levels
# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL
LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s', level=LOG_LEVEL) 

logger = logging.getLogger(__name__)

def init():
   
    global use_gui
    use_gui = False 

    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    global WIDGET_WIDTH, WIDGET_HEIGHT
    WIDGET_WIDTH = WIDGET_HEIGHT = 32

    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)

    global background
    background = pygame.Surface(screen.get_size())


    global icon_arr
    icon_arr = [pygame.image.load("icons/"+str(z+1)+".png") for z in range(7)]
    icon_arr.append(pygame.image.load("icons/unbroken.png"))
    icon_arr.append(pygame.image.load("icons/cracked.png"))

    # global font
    # font = pygame.font.Font(None, 12)

    global BLACK, WHITE
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


    global gui
    gui = Gui()


    

    global game_iterations, totaled_scores, highest_score, totaled_longest_combo, highest_longest_combo
    game_iterations = 100
    totaled_scores = 0
    highest_score = 0
    totaled_longest_combo = 0
    highest_longest_combo = 0

    game_setup()


def game_setup():

    # Dynamic variables
    global combo_modifier, score, longest_combo, level, level_widgets_remaining, game_over, combo_list
    combo_modifier = 0
    score = 0
    longest_combo = 0
    level = 1
    #level_widgets_remaining = BASE_LEVEL_WIDGET_COUNT
    level_widgets_remaining = 3
    game_over = False
    combo_list = [7, 39, 109, 224, 391, 617, 907, 1267, 1701, 2213, 2809, 3491, 4265, 5133, 6099, 7168, 8341, 9622, 11014, 12521, 14146, 15891, 17758, 19752, 21875, 24128, 26515, 29039, 31702, 34506]