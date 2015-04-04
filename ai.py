import logging
import random
import time
import pygame


logger = logging.getLogger(__name__)

class AI:
    board = None
    widget_number = None
    possible_moves = None
    priority_moves = None
    priority_explanations = None

    def __init__(self):
        return

    def home(self, board, widget_number):
        self.possible_moves = [0, 1, 2, 3, 4, 5, 6]
        self.priority_moves = [0, 0, 0, 0, 0, 0, 0]
        self.priority_explanations = [[] for i in xrange(7)]

    
        self.board = board
        self.widget_number = widget_number

        self.check_column_full()

        for case in switch(self.widget_number):
            if case(1): 
                self.widget_1()
                break
            if case(2):
                self.widget_2()
                break
            if case(3): 
                self.widget_3()
                break
            if case(4):
                self.widget_4()
                break
            if case(5): 
                self.widget_5()
                break
            if case(6):
                self.widget_6()
                break
            if case(7): 
                self.widget_7()
                break
            if case(): # default
                self.widget_unbroken()
                logger.debug("default case")


        if len(self.possible_moves) > 1:
            self.remove_impossible_moves()
            rand_index = self.weighted_choice(self.priority_moves)
            logger.debug("# possible moves: %d", len(self.possible_moves))
            move_x_coordinate = rand_index
        elif len(self.possible_moves) == 1:
            move_x_coordinate = self.possible_moves[0]
        else:
            for row in self.board:
                for val in row:
                    if val is not None:
                        #logger.info(val.number)
                        print '{:4}'.format(val.number),
                    else:
                        #logger.info("0")
                        print '{:4}'.format(0),
                print "\n"

            top_row_full = True
            for x in range(7):
                if self.board[0][x] is None:
                    top_row_full = False

            if top_row_full:
                pygame.time.wait(1000)
                return -10

        move = move_x_coordinate - 3
        return move

    def remove_impossible_moves(self):
        for x in range(7):
            if self.possible_moves.count(x) == 0:
                self.priority_moves[x] = None

    def weighted_choice(self, weights):
        #weights = [x for x in weights if x is not None]

        minimum = min(weights)

        minimum = min(i for i in weights if i is not None)

        offset = 0;

        if minimum <= 0:
            
            offset = minimum * -1

        if max(weights) == 0 and minimum == 0:
            offset += 1

        for i, val in enumerate(weights):
            if weights[i] is not None:
                weights[i] += offset
        
        for msgs in self.priority_explanations:
            logger.debug("")
            for msg in msgs:
                logger.debug(msg)


        minimum = min(i for i in weights if i is not None)

        if max(weights) == 0 and minimum == 0:
            for i, w in enumerate(weights):
                weights[i] = 1;

        totals = []
        running_total = 0

        weights = AI.analyze_weights(weights)

        logger.debug(weights)

        for w in weights:
            if w is not None:
                running_total += w
            totals.append(running_total)

        rnd = random.random() * running_total

        for i, total in enumerate(totals):
            if rnd < total:
                return i

    @staticmethod
    def analyze_weights(weights):
        maximum = max(weights)
        minimum = min(weights)
        weights = [(x if x is not None else 0) for x in weights]

        avg = sum(weights)/len(weights)

        removed_below_average = False
        for idx, weight in enumerate(weights):
            if weight < avg:
                removed_below_average = True
                weights[idx] = 0
        if removed_below_average:
            logger.debug("Remove below average")


        if maximum > avg*2:
            logger.debug("")
            logger.debug("Analyze Weights: Outlier Max")
            for idx, weight in enumerate(weights):
                if weights[idx] != maximum:
                    weights[idx] = 0

        return weights


    def check_column_full(self):
        for x in range(7):
            if self.board[0][x] is not None:
                self.possible_moves.remove(x)

    def width_break(self, widget_number):
        break_priority = 50
        no_break_priority = -25

        column_heights = self.find_column_heights()

        for idx, height in enumerate(column_heights):
            if self.adjacent_widgets(idx, 6-height, horizontal_check=True) + 1 == widget_number:
                self.priority_moves[idx] += break_priority
                self.priority_explanations[idx].append("Column {0}:\t+{1}: {2} width location".format(idx, break_priority, widget_number-1))
            else:
                self.priority_moves[idx] += no_break_priority
                self.priority_explanations[idx].append("Column {0}:\t{1}: !{2} width location".format(idx, no_break_priority, widget_number-1))

    def height_break(self, widget_number):
        break_priority = 100
        no_break_priority = -75

        column_heights = self.find_column_heights()

        logger.debug("column heights:")
        logger.debug(column_heights)

        for idx, height in enumerate(column_heights):
            if column_heights[idx] + 1 == widget_number:
                self.priority_moves[idx] += break_priority
                self.priority_explanations[idx].append("Column {0}:\t+{1}: {2} height location".format(idx, break_priority, widget_number-1))
            else:
                self.priority_moves[idx] += no_break_priority
                self.priority_explanations[idx].append("Column {0}:\t{1}: !{2} height location".format(idx, no_break_priority, widget_number-1))

        top = True


    def column_width_priority(self, widget_number):
        column_heights = self.find_column_heights()
        column_horizontal_adjacents = [0, 0, 0, 0, 0, 0, 0]

        for idx, height in enumerate(column_heights):
            column_horizontal_adjacents[idx] = self.adjacent_widgets(idx, 6-height, horizontal_check=True)

        for x in range(len(column_horizontal_adjacents)):
            priority = (widget_number - column_horizontal_adjacents[x] - 1) * 20
            self.priority_moves[x] += priority
            self.priority_explanations[x].append("Column {0}:\t{1}: {2} horizontally adjacent widgets".format(x, priority, column_horizontal_adjacents[x]))


    def column_height_priority(self, widget_number):

        column_heights = self.find_column_heights()

        for x in range(len(column_heights)):    
            priority = (widget_number - column_heights[x] - 1) * 20
            self.priority_moves[x] += priority
            self.priority_explanations[x].append("Column {0}:\t{1}: {2} height column".format(x, priority, column_heights[x]))


    def find_column_heights(self):
        column_heights = [0, 0, 0, 0, 0, 0, 0]

        for x in range(7):
            for y in reversed(range(7)):
                if self.board[y][x] is None:
                    column_heights[x] = 6-y
                    break

        return column_heights

    def widget_unbroken(self):
        # Drop somewhere it will be cracked/broken

        # Do not drop onto an unbroken or cracked widget
        column_heights = self.find_column_heights()

        adjacent_unbroken = [0, 0, 0, 0, 0, 0, 0]
        adjacent_cracked = [0, 0, 0, 0, 0, 0, 0]
        adjacent_number = [0, 0, 0, 0, 0, 0, 0]
        for idx, height in enumerate(column_heights):
            if idx > 0:
                if self.board[idx-1][height] is not None:
                    if self.board[idx-1][height].unbroken:
                        adjacent_unbroken[idx] += 1
                    elif self.board[idx-1][height].cracked:
                        adjacent_cracked[idx] += 1
                    else:
                        adjacent_number[idx] += 1
            if idx < 6:
                if self.board[idx+1][height] is not None:
                    if self.board[idx+1][height].unbroken:
                        adjacent_unbroken[idx] += 1
                    elif self.board[idx+1][height].cracked:
                        adjacent_cracked[idx] += 1
                    else:
                        adjacent_number[idx] += 1
            if height > 0:
                if self.board[idx][height-1] is not None:
                    if self.board[idx][height-1].unbroken:
                        adjacent_unbroken[idx] += 1
                    elif self.board[idx][height-1].cracked:
                        adjacent_cracked[idx] += 1
                    else:
                        adjacent_number[idx] += 1
            if height < 6:
                if self.board[idx][height+1] is not None:
                    if self.board[idx][height+1].unbroken:
                        adjacent_unbroken[idx] += 1
                    elif self.board[idx][height+1].cracked:
                        adjacent_cracked[idx] += 1
                    else:
                        adjacent_number[idx] += 1   

        priority = [0, 0, 0, 0, 0, 0, 0]

        for idx, val in enumerate(priority):
            priority[idx] -= 2*adjacent_unbroken[idx]
            priority[idx] -= 1*adjacent_cracked[idx]
            priority[idx] += 1*adjacent_number[idx]
            priority[idx] *= 20
            self.priority_moves[idx] += priority[idx]


    def widget_1(self):
        self.height_break(1)
        self.column_height_priority(1)
        self.width_break(1)
        self.column_width_priority(1)


    def widget_2(self):
        self.height_break(2)
        self.column_height_priority(2)
        self.width_break(2)
        self.column_width_priority(2)


    def widget_3(self):
        self.height_break(3)
        self.column_height_priority(3)
        self.width_break(3)        
        self.column_width_priority(3)

    def widget_4(self):
        self.height_break(4)
        self.column_height_priority(4)
        self.width_break(4)        
        self.column_width_priority(4)

    def widget_5(self):
        self.height_break(5)
        self.column_height_priority(5)
        self.width_break(5)        
        self.column_width_priority(5)

    def widget_6(self):
        self.height_break(6)
        self.column_height_priority(6)
        self.width_break(6)        
        self.column_width_priority(6)

    def widget_7(self):
        self.height_break(7)
        self.column_height_priority(7)
        self.width_break(7)        
        self.column_width_priority(7)

    def adjacent_widgets(self, x, y, left_check=False, right_check=False, up_check=False, down_check=False, horizontal_check=False, vertical_check=False):
        adjacent_widgets = 0
        if horizontal_check:
            left_check = True
            right_check = True
        if vertical_check:
            up_check = True
            down_check = True

        if left_check:
            if x >= 1:
                widget = self.board[y][x-1]
                if widget != None:
                    adjacent_widgets += 1 + self.adjacent_widgets(x-1, y, left_check=True)
        if right_check:
            if x <= 5:
                widget = self.board[y][x+1]
                if widget != None:
                    adjacent_widgets += 1 + self.adjacent_widgets(x+1, y, right_check=True)

        if down_check:
            if y >= 1:
                widget = self.board[y-1][x]
                if widget != None:
                    adjacent_widgets += 1 + self.adjacent_widgets(x, y-1, down_check=True)
        if up_check:
            if y <= 5:
                widget = self.board[y+1][x]
                if widget != None:
                    adjacent_widgets += 1 + self.adjacent_widgets(x, y+1, up_check=True)

        return adjacent_widgets



    def x_coordinate_to_right_moves(self, x, home_x=3):
        right_moves = 0

        diff = x - home_x


        return right_moves


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False