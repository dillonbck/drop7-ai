"""
File: widget.py
Author: Dillon Beck

Classes:
    Widget: Manages widget attributes.

"""
import logging
import pygame
from random import randint
import config
from eventmanager import *


LOGGER = logging.getLogger(__name__)

class Widget(object):
    """Widget class that manages breaking/cracking widgets and movement.

    #TODO: loc_x and loc_y -> (loc_X, loc_y) or (row, column)

    Attribute:
        number: Int representing the number of the widget.
        unbroken: Boolean indicating whether widget is unbroken.
        cracked: Boolean indicating whether widget is cracked.
        sprite: Sprite for the widget.
        loc_x: Row the widget occupies.
        loc_y: Column the widget occupies.
        active: Whether the widget is the one being moved by the user.
        delete: Whether the widget is deleted or not.
    """

    UNBROKEN = 2
    CRACKED = 1
    BROKEN = 0

    def __init__(self, game_engine, unbroken=False, row=0, column=0):

        self.game_engine = game_engine
        self.number = randint(1, 7)

        if unbroken or (randint(1, 8) == 8):    # mostly broken
            self.state = Widget.UNBROKEN

            if config.use_gui:
                self.sprite = config.icon_arr[7]
        else:
            self.state = Widget.BROKEN
            
            if config.use_gui:
                self.sprite = config.icon_arr[self.number - 1]

        if unbroken:
            self.loc_x = row
            self.loc_y = column
            self.active = 0
        else:
            self.loc_x = self.game_engine.DROP_X
            self.loc_y = self.game_engine.DROP_Y
            self.active = 1

        self.delete = 0

        event = WidgetCreateEvent()
        event.active_widget = self.active
        event.loc_x = self.loc_x
        event.loc_y = self.loc_y
        event.state = self.state
        event.number = self.number 

        self.game_engine.evManager.Post(event)

    def clear(self):
        """Remove the widget from the screen.

        #TODO: This is gui stuff...

        """

        event = WidgetClearEvent()
        event.active_widget = self.active
        event.loc_x = self.loc_x
        event.loc_y = self.loc_y

        self.game_engine.evManager.Post(event)


    def right(self):
        """Move the widget right 1 spot.

        The widget will move right 1 spot, but its x location will not be 
        greater than 7.

        """

        if self.loc_x < 6 and self.active == 1:
            self.loc_x += 1


    def left(self):
        """Move the widget left 1 spot.

        The widget will move left 1 spot, but its x location will not be less
        than 0.

        """

        if self.loc_x >= 1 and self.active == 1:
            self.loc_x -= 1

            # self.redraw(prev_x=self.loc_x+1)
    

    # Mark a cell to be deleted
    def remove(self):
        """Mark a widget as deleted.
        #TODO: Should this even be a method?
        #TODO: Should/can this be renamed to delete?
        """

        self.delete = 1

        if config.use_gui:
            self.clear()
            pygame.time.wait(100)


    # def check_break(self):
    #     new_sprite = None

    #     if  self.cracked == True:
    #         self.cracked = False
    #         if config.use_gui:
    #             new_sprite = config.icon_arr[self.number - 1]
    #         #self.sprite = config.icon_arr[self.number - 1]
    #         #self.draw()
    #     if self.unbroken == True:
    #         self.unbroken = False
    #         self.cracked = True
    #         if config.use_gui:
    #             new_sprite = config.icon_arr[8]
    #         #self.sprite = config.icon_arr[8]
    #         #self.draw()

    #     if config.use_gui:
    #         if new_sprite is not None:
    #             self.sprite = new_sprite
    #             self.draw()


    def check_break(self):
        """Break or crack the widget.

        Check if the widget is unbroken or cracked.  If unbroken, crack the 
        widget.  If cracked, break the widget.  If broken, do nothing.
        Updates the widget's sprite.

        """

        changed = False

        if self.state == Widget.CRACKED:
            self.state = Widget.BROKEN
            changed = True

        if self.state == Widget.UNBROKEN:
            self.state = Widget.CRACKED
            changed = True


        if changed:
            move_event = WidgetMoveEvent()
            move_event.prev_x = self.loc_x
            move_event.cur_x = self.loc_x
            move_event.prev_y = self.loc_y
            move_event.cur_y = self.loc_y
            move_event.prev_active = self.active
            move_event.cur_active = self.active
            move_event.state = self.state
            move_event.number = self.number

            self.game_engine.evManager.Post(move_event)

        # if  self.cracked == True:
        #     self.cracked = False

        # if self.unbroken == True:
        #     self.unbroken = False
        #     self.cracked = True
