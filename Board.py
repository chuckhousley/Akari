import random

global_x = 0
global_y = 0


class Board:
    board = {}

    def __init__(self, file_input):
        global global_x
        global_x = file_input.x
        global global_y
        global_y = file_input.y
        for i in range(global_x):
            for j in range(global_y):
                self.board[(i, j)] = 6

        for i in file_input.block_list:
            self.board[(i[0], i[1])] = i[2]
