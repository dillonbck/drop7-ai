"""
File: board.py
Author: Dillon Beck

Classes:
    Board: Manages widgets on the board and level up and scoring.

"""
import logging
import pygame
from eventmanager import *

from widget import Widget


LOGGER = logging.getLogger(__name__)

class Board(object):
    """Board class that manages dropping, breaking, and removing widgets and 
        level up and scoring mechanics.

    Attribute:
        arr: Two dimensional array representing the board containing widgets. 
        widget_count: Int representing number of widgets on the board.

    """


    def __init__(self, game_engine):
        """Initialize empty board."""

        self.arr = [[None for x in range(7)] for y in range(7)]
        self.widget_count = 0
        self.game_engine = game_engine

    # Check to see if the widget at the specified location will be destroyed
    def check_cell(self, x_loc, y_loc):
        """Check if the widget at specified location will be destroyed.

        Check if the widget at the specified location is subject to destruction:
            widget's number == number of widgets currently in the row or column.


        Args:
            argument: Explanation.
            x_loc: X (column) location of widget to check.
            y_loc: Y (row) location of widget to check.

        Returns:
            Returns a boolean indicating whether the widget at the specified 
            location will be destroyed.

        """
        if self.arr[y_loc][x_loc] is not None and self.arr[y_loc][x_loc].state == Widget.BROKEN:
            LOGGER.debug("\nnumber: %d", self.arr[y_loc][x_loc].number)

            # Check horizontal widget removals
            length = 1
            i = x_loc - 1
            while i >= 0 and self.arr[y_loc][i] != None:
                length += 1
                i -= 1
            i = x_loc + 1
            while i <= 6 and self.arr[y_loc][i] != None:
                length += 1
                i += 1

            LOGGER.debug("horizontal check:")
            LOGGER.debug("length == number?: %d == %d: %d", 
                         length, self.arr[y_loc][x_loc].number, 
                         length == self.arr[y_loc][x_loc].number)
            #if self.arr[y_loc][x_loc].state == Widget.BROKEN and length == self.arr[y_loc][x_loc].number:
            if length == self.arr[y_loc][x_loc].number:
                self.arr[y_loc][x_loc].remove()  # Destroy this widget
                self.widget_count -= 1

                # check if adjacent widgets are unbroken and if so crack them
                self.check_adjacent(x_loc, y_loc)
                #pygame.time.wait(1000)
                return True

            # Check vertical widget removals
            i = y_loc - 1
            length = 1
            while i >= 0 and self.arr[i][x_loc] != None:
                length += 1
                i -= 1
            i = y_loc + 1
            while i <= 6 and self.arr[i][x_loc] != None:
                length += 1
                i += 1
            LOGGER.debug("vertical check:")
            LOGGER.debug("length == number?: %d == %d: %d", 
                         length, self.arr[y_loc][x_loc].number, 
                         length == self.arr[y_loc][x_loc].number)
            if length == self.arr[y_loc][x_loc].number:
                self.arr[y_loc][x_loc].remove()
                self.widget_count -= 1

                # check if adjacent widgets are unbroken and if so crack them
                self.check_adjacent(x_loc, y_loc)
                #pygame.time.wait(1000)
                return True

            pygame.time.wait(500)
            return False

    def check_adjacent(self, x_loc, y_loc):
        """Check if widgets adjacent to specified location will break or crack. 

        For each location adjacent to the specified location, check if there is
        a widget, and if so, check if it will break or crack.
        Will crack any unbroken widgets adjacent to specified location.
        Will break any cracked widgets adjacent to specified location.

        Args:
            x_loc: X (column) location to check adjacent.
            y_loc: Y (row) location to check adjacent. 

        """
        if x_loc >= 1:
            widget = self.arr[y_loc][x_loc-1]
            if widget != None:
                widget.check_break()
        if x_loc <= 5:
            widget = self.arr[y_loc][x_loc+1]
            if widget != None:
                widget.check_break()
        if y_loc >= 1:
            widget = self.arr[y_loc-1][x_loc]
            if widget != None:
                widget.check_break()
        if y_loc <= 5:
            widget = self.arr[y_loc+1][x_loc]
            if widget != None:
                widget.check_break()






    def drop(self, widget):
        """Drop the active widget down its current column until it lands.

        The active widget (next widget being controlled by the user to be 
        dropped) is dropped down the column where it currently resides until it
        lands.
        If the widget can not be dropped in the current column (column is full),
        this method will return false.

        Args:
            widget: The widget being dropped.

        Returns:
            A boolean indicating whether the widget was dropped.

        """

        if widget.active == 1:
            if self.arr[widget.loc_y][widget.loc_x] != None:
                return False

            # Drop until widget lands
            while widget.loc_y < 6 and self.arr[widget.loc_y + 1][widget.loc_x] == None:
                #self.clear()      # Erase where widget was
                widget.loc_y += 1         # Move down 1 spot
                #self.draw()       # Redraw screen


            self.arr[widget.loc_y][widget.loc_x] = widget    # Lock in the widget's position
            #self.clear()
            widget.active = 0     # Widget is now inactive
            #self.draw()       # Redraw screen

            self.widget_count += 1

            return True



    def scoot(self):
        """Find all floating widgets and drop them to their final resting place.

        Starting with the bottom row, find any widget with an empty space below
        it and move it down until there is no empty space below it.  Repeat 
        until no widgets have an empty space below.

        Returns:
            A boolean indicating whether the board changed from this operation.

        """

        board_changed = False
        for row in range(7):
            for column in reversed(range(6)):
                widget = self.arr[column][row]
                next_spot = self.arr[column+1][row]
                column_copy = column 

                while widget != None and next_spot == None and column_copy <= 5:
                    
                    my_widget = self.arr[column_copy][row]
                    #my_widget.clear()

                    #pygame.time.wait(200)

                    my_widget.loc_y += 1
                    self.arr[column_copy + 1][row] = my_widget 
                    self.arr[column_copy][row] = None

                    #myWidget.redraw(prev_y=myWidget.loc_y-1)

                    move_event = WidgetMoveEvent()
                    move_event.prev_x = row
                    move_event.cur_x = row
                    move_event.prev_y = column_copy
                    move_event.cur_y = column_copy + 1
                    move_event.prev_active = my_widget.active
                    move_event.cur_active = my_widget.active
                    move_event.state = my_widget.state
                    move_event.number = my_widget.number

                    self.game_engine.evManager.Post(move_event)


                    board_changed = True
                    
                    widget = self.arr[column_copy+1]
                    if column_copy+2 <= 6:
                        next_spot = self.arr[column_copy+2][row]
                    column_copy += 1

                    

        if board_changed:
            pygame.time.wait(100)

            self.scoot()
        return board_changed


    def clean(self):
        """Remove all widgets marked for deletion from the board and score.

        Iterate through each spot on the board and find all widgets marked for
        deletion.  Remove them from the board and score points for them.

        Returns:
            A boolean indicating whether the board has changed.

        """
        board_changed = False
        for row in range(7):
            for column in range(7):
                if (self.arr[column][row] != None and 
                        self.arr[column][row].delete == 1):
                    if self.game_engine.combo_modifier > 0:
                        LOGGER.debug("Combo %d\n\tScore += %d", 
                                     self.game_engine.combo_modifier, 
                                     self.game_engine.COMBO_LIST[
                                         self.game_engine.combo_modifier])

                    self.game_engine.score += \
                        self.game_engine.COMBO_LIST[self.game_engine.combo_modifier]

                    board_changed = True
                    self.arr[column][row].clear()
                    self.arr[column][row] = None

        if board_changed:
            self.game_engine.combo_modifier += 1

        return board_changed


    def check(self):
        """Remove any deleted widgets and move widgets until board is stable.

        Iterate through each board spot and remove any deleted widgets.
        Check if any widgets are floating and drop them until no widgets are 
        floating.
        This method will repeat until a stable state (no widgets floating and
        all deleted widgets removed) is reached. 

        """

        board_changed = False

        # Check each cell to see if the widget will be destroyed
        for row in range(7):
            for column in range(7):
                if self.check_cell(row, column) == True:
                    board_changed = True

        if board_changed:
            self.clean()
            self.scoot()
            self.check()

        if self.game_engine.combo_modifier > self.game_engine.longest_combo:
            self.game_engine.longest_combo = self.game_engine.combo_modifier
        self.game_engine.combo_modifier = 0

            
    def add_unbroken_row(self):
        """Move all widgets up 1 row and fill bottom row with unbroken widgets.

        All widgets are moved up 1 row and the bottom row is filled with 
        unbroken widgets.

        No check is made to see if the board will overflow (top row moves off
        the board), so this method assumes a check is made beforehand.

        """

        for row in range(7):
            for column in range(7):
                widget = self.arr[column][row]

                if widget is not None:
                    #widget.clear()
                    widget.loc_y -= 1
                    self.arr[column-1][row] = widget
                    self.arr[column][row] = None

                    move_event = WidgetMoveEvent()
                    move_event.prev_x = row
                    move_event.cur_x = row
                    move_event.prev_y = column
                    move_event.cur_y = column - 1
                    move_event.prev_active = widget.active
                    move_event.cur_active = widget.active
                    move_event.state = widget.state
                    move_event.number = widget.number

                    self.game_engine.evManager.Post(move_event)

        for row in range(7):
            widget = Widget(self.game_engine, True, row, 6)
            self.arr[6][row] = widget

        self.print_board()
        #pygame.display.flip()
        self.check()
        self.widget_count += 7

    def level_check(self):
        """Check if the next level has been reached.

        Decrement the number of widgets remaining to complete the current level,
        and if the number of remaining widgets for the level is 0, increment
        to the next level.
        Each level requires 1 less widget to be dropped to reach the next level.
        The number of widgets needed to be dropped to reach the next level can
        only be decremented to a specified number - no less than this number of 
        widgets will ever be required to reach the next level.

        """

        self.game_engine.level_widgets_remaining -= 1

        # Finished level widgets, level up - add unbroken row
        #if config.level_widgets_remaining == 0:
        if self.game_engine.level_widgets_remaining == 0:
            self.game_engine.level += 1
            self.game_engine.score += 7000
            self.game_engine.level_widgets_remaining = \
                (self.game_engine.BASE_LEVEL_WIDGET_COUNT - 
                 self.game_engine.level + 1)

            #config.level += 1
            #config.score += 7000
            #config.level_widgets_remaining = 
            #   self.game_engine.BASE_LEVEL_WIDGET_COUNT - config.level + 1
            if (self.game_engine.level_widgets_remaining < 
                    self.game_engine.MINIMUM_LEVEL_WIDGET_COUNT):
                self.game_engine.level_widgets_remaining += 1
            #self.check_game_over(row_add=True)
            self.check_game_over(row_add=True)
            self.add_unbroken_row()

    def check_game_over(self, row_add=False):
        """Check conditions for the game to end.

        Check the two conditions for which the game will end.
        If the entire top row is full, no more widgets can be dropped and the 
        game is over.
        If a new row of unbroken widgets is about to be added (level up) and 
        there is a widget in the top row of the board (that will overflow on the
        level up), the game is over.
        Sets config.game_over to indicate game is over.

        Args:
            row_add: Boolean indicating whether this game over check should 
                consider that a row of widgets is about to be added to the 
                bottom row and all other widgets are being pushed up.

        """

        if row_add:
            for row in range(7):
                if self.arr[0][row] is not None:
                    self.game_engine.game_over = True
                    self.game_engine.running = False
        elif not row_add:
            top_row_full = True
            for row in range(7):
                if self.arr[0][row] is None:
                    top_row_full = False

            if top_row_full:
                self.game_engine.game_over = True
                self.game_engine.running = False

        if self.game_engine.game_over:
            LOGGER.info("Game Over!\nScore: %d\nLevel: %d\nLongest Combo: %d", 
                        self.game_engine.score, self.game_engine.level, 
                        self.game_engine.longest_combo)



    def print_board(self):
        """Print out a text representation of the board's current status.

        Log debug messages that show the current widget numbers occupying each
        spot.

        """

        for row in self.arr:
            for val in row:
                if val is not None:
                    LOGGER.debug("%4d", val.number)
                    #LOGGER.debug('{:4}'.format(val.number))
                    #print '{:4}'.format(val.number),
                else:
                    LOGGER.debug("%4d", 0)
                    #LOGGER.debug('{:4}'.format(0))
                    #print '{:4}'.format(0),
# end Board class
