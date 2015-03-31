import logging

import pygame

import config


logger = logging.getLogger(__name__)

class Gui():
    def __init__(self):
        i = 0

    @staticmethod
    def setup():
        pygame.display.set_caption('Drop7')


    @staticmethod
    def printGameInfo(score, level, remaining_widgets):
        Gui.printScore(score)
        Gui.printLevel(level)
        Gui.printRemainingWidgets(remaining_widgets)


    @staticmethod
    def printScore(score):
        text = config.font.render("Score: " + str(score), 1, config.WHITE)
        textpos = text.get_rect(left=0)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)


    @staticmethod
    def printLevel(level):
        text = config.font.render("Level: " + str(level), 1, config.WHITE)
        textpos = text.get_rect(top=12)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)


    @staticmethod
    def printRemainingWidgets(remaining_widgets):
        text = config.font.render("Remaining Widgets: " + str(remaining_widgets), 1, config.WHITE)
        textpos = text.get_rect(top=24)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)




