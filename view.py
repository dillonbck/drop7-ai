import pygame
from pygame.locals import *
import model
from eventmanager import *
import config
from widget import Widget

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
        self.dirty_rects = []

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, InitializeEvent):
            self.initialize()

        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()

        elif isinstance(event, TickEvent):
            self.renderall()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

        elif isinstance(event, WidgetMoveEvent):
            prev_x = event.prev_x
            cur_x = event.cur_x
            prev_y = event.prev_y
            cur_y = event.cur_y
            prev_active = event.prev_active
            cur_active = event.cur_active
            state = event.state
            number = event.number

            self.redraw(prev_x, cur_x, prev_y, cur_y, prev_active, cur_active, state, number)

        elif isinstance(event, WidgetCreateEvent):
            active_widget = event.active_widget
            loc_x = event.loc_x
            loc_y = event.loc_y
            state = event.state
            number = event.number

            self.draw_widget(active_widget, loc_x, loc_y, state, number)

        elif isinstance(event, WidgetClearEvent):
            active_widget = event.active_widget
            loc_x = event.loc_x
            loc_y = event.loc_y

            self.clear_widget(active_widget, loc_x, loc_y)

            print("handling WidgetCreateEvent")


    def renderall(self):
        """
        Draw the current game state on screen.
        Uses dirty rectangle updating - Only update screen where changes happened.
        Does nothing if isinitialized == False (pygame.init failed)
        """

        if not self.isinitialized:
            return
        # # clear display
        # self.screen.fill((0, 0, 0))
        # # draw some words on the screen
        # somewords = self.smallfont.render(
        #             'The View is busy drawing on your screen', 
        #             True, 
        #             (0, 255, 0))
        # self.screen.blit(somewords, (0, 0))
        # flip the display to show whatever we drew
        #pygame.display.flip()

        pygame.display.update(self.dirty_rects)
        self.dirty_rects = []

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((600, 60))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), DOUBLEBUF)


    def redraw(self, prev_x, cur_x, prev_y, cur_y, prev_active, cur_active, state, number):
        self.clear_widget(prev_active, prev_x, prev_y)
        self.draw_widget(cur_active, cur_x, cur_y, state, number)


    # def redraw(self, prev_x=None, prev_y=None, prev_active=None):
    #     if prev_x is None:
    #         prev_x = self.loc_x
    #     if prev_y is None:
    #         prev_y = self.loc_y
    #     if prev_active is None:
    #         prev_active = self.active

    #     if config.use_gui:
    #         config.gui.clear_widget(prev_active, prev_x, prev_y)
    #         config.gui.draw_widget(self.sprite, self.active, self.loc_x, self.loc_y)


    def clear_widget(self, active_widget, loc_x, loc_y):
        if active_widget:
            y = loc_y+1
        else:
            y = loc_y+2

        box = pygame.Rect(loc_x * config.WIDGET_WIDTH, y * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)
        pygame.draw.rect(config.screen, config.BLACK, box, 0)
        self.dirty_rects.append(box)



    def draw_widget(self, active_widget, loc_x, loc_y, state, number):
        # if active_widget:
        #     config.screen.blit(sprite, (loc_x * config.WIDGET_WIDTH, (loc_y+1) * config.WIDGET_HEIGHT))
        # else:
        #     config.screen.blit(sprite, (loc_x * config.WIDGET_WIDTH, (loc_y+2) * config.WIDGET_HEIGHT))

        if active_widget:
            y_modifier = 1
        else:
            y_modifier = 2

        sprite = self.find_widget_sprite(state, number)
        loc = (loc_x * config.WIDGET_WIDTH, (loc_y+y_modifier) * config.WIDGET_HEIGHT)

        config.screen.blit(sprite, loc)



        size = (config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)
        box = pygame.Rect(loc, size)
        self.dirty_rects.append(box)


    def find_widget_sprite(self, state, number):
        if state == Widget.UNBROKEN:
            sprite = config.icon_arr[7]
        elif state == Widget.CRACKED:
            sprite = config.icon_arr[8]
        elif state == Widget.BROKEN:
            sprite = config.icon_arr[number - 1]

        return sprite
