import pygame
from eventmanager import *

from board import Board
from widget import Widget
import config




class GameEngine(object):
    """
    Tracks the game state.
    """

    BASE_LEVEL_WIDGET_COUNT = 30
    MINIMUM_LEVEL_WIDGET_COUNT = 5

    DROP_X = 3
    DROP_Y = 0

    COMBO_LIST = [7, 39, 109, 224, 391, 617, 907, 1267, 1701, 2213, 2809, 3491, 
                  4265, 5133, 6099, 7168, 8341, 9622, 11014, 12521, 14146, 
                  15891, 17758, 19752, 21875, 24128, 26515, 29039, 31702, 34506]


    def __init__(self, evManager):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False

        self.combo_modifier = 0
        self.score = 0
        self.longest_combo = 0
        self.level = 1
        self.level_widgets_remaining = GameEngine.BASE_LEVEL_WIDGET_COUNT

        self.game_over = False

        self.board = Board(self)

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event, QuitEvent):
            self.running = False


        elif isinstance(event, MoveEvent):
            move_event = WidgetMoveEvent()
            move_event.prev_x = self.active_widget.loc_x
            move_event.prev_y = self.active_widget.loc_y
            move_event.prev_active = self.active_widget.active

            if event.direction == MoveEvent.DIR_LEFT:
                self.active_widget.left()

            elif event.direction == MoveEvent.DIR_RIGHT:
                self.active_widget.right()

            elif event.direction == MoveEvent.DIR_DOWN:
                self.board.drop(self.active_widget)


            move_event.cur_x = self.active_widget.loc_x
            move_event.cur_y = self.active_widget.loc_y
            move_event.cur_active = self.active_widget.active
            move_event.state = self.active_widget.state
            move_event.number = self.active_widget.number

            self.evManager.Post(move_event)


            if event.direction == MoveEvent.DIR_DOWN:
                self.board.check()

                self.board.check_game_over()
                self.board.level_check()
                

                if self.game_over:
                    self.evManager.Post(QuitEvent())
                    #break
                #logger.debug("widget_count: %d", self.board.widget_count)
                self.board.print_board()

                self.active_widget = Widget(self)



    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(InitializeEvent())
        self.active_widget = Widget(self)

        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)

