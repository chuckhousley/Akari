from random import Random


class Board:
    board = {}
    max_x = None
    max_y = None
    rand = None

    def __init__(self, file_input):
        self.max_x = file_input.x
        self.max_y = file_input.y
        for i in range(self.max_x):
            for j in range(self.max_y):
                self.board[(i+1, j+1)] = 6

        for i in file_input.block_list:
            self.board[(i[0], i[1])] = i[2]

        self.rand = Random(file_input.seed)

