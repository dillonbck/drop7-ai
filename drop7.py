import logging
import pygame, sys, os
from pygame.locals import *

import config
from widget import Widget
from board import Board
from ai import AI


logger = logging.getLogger("Drop7")

##### Game stuff #####
pygame.init()                   # Initialization
config.init()   # Instantiate global variables in config

if config.use_gui:
    clock = pygame.time.Clock()

    config.gui.setup()


for x in range(config.game_iterations):
    board = Board()
    active_widget = Widget()

    ai = AI()

    while 1:
        if config.use_gui:
            clock.tick(30)

        board.check_game_over
        if config.game_over:
            #sys.exit(0)
            break

        # AI Input
        ai_widget_number = active_widget.number
        if active_widget.unbroken:
            ai_widget_number = 0
        logger.debug("widget number: %d", ai_widget_number)
        ai_move = ai.home(board.arr, ai_widget_number)
        if ai_move == -10:
            config.game_over
            break
        
        #pygame.time.wait(2000)

        #raw_input()

        while (ai_move != 0):
            if ai_move < 0:
                active_widget.left()
                ai_move += 1
            else:
                active_widget.right()
                ai_move -= 1

        #if active_widget.drop(board) == True:
        if board.drop(active_widget) == True:
            board.check_game_over()
            board.widget_count += 1
            active_widget = Widget()
            board.check()
            board.level_check()
            if config.game_over:
                #sys.exit(0)
                break
            logger.debug("widget_count: %d", board.widget_count)
            if config.use_gui:
                config.gui.printGameInfo(config.score, config.level, config.level_widgets_remaining)



        # User Input
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            if not hasattr(event, 'unicode'):
                continue
            if event.key == K_RIGHT:
                active_widget.right()
            elif event.key == K_LEFT:
                active_widget.left()
            elif event.key == K_DOWN:
                # If widget fits on the chosen column
                if active_widget.drop(board) == True:
                    board.check_game_over()
                    board.widget_count += 1
                    active_widget = Widget()
                    board.check()
                    board.level_check()
                    if board.game_over:
                        sys.exit(0)
                    logger.debug("widget_count: %d", board.widget_count)    
            elif event.key == K_ESCAPE or event.key == K_q: 
                sys.exit(0)
            elif event.key == K_UP:
                print board.arr
                board.add_unbroken_row()

        if config.use_gui:
            # Rendering
            pygame.display.flip()


    config.totaled_scores += config.score
    config.totaled_longest_combo += config.longest_combo

    if config.score > config.highest_score:
        config.highest_score = config.score
    if config.longest_combo > config.highest_longest_combo:
        config.highest_longest_combo = config.longest_combo

    config.game_setup()

logger.info("Average Score: %d", config.totaled_scores/config.game_iterations)
logger.info("Highest Score: %d", config.highest_score)
logger.info("Average Longest Combo: %0.2f", config.totaled_longest_combo/float(config.game_iterations))
logger.info("Highest Longest Combo: %d", config.highest_longest_combo)