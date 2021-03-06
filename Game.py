from random import Random
from get_boxes import get_all, get_all_unlit, get_neighbors, get_neighbor_values
from functions import place_light, update_tile
import g

##class notes on Game:
#board is a dict so any tile can be accessed using board[(x, y)]
#tiles can have 10 different values:
#0-4: black box with corresponding number
#5: black box with no number
#6: unlit tile
#7: lit tile
#8: light bulb tile
#9: light bulb tile that is being lit by another light bulb (mutually lit)


class Game:
    board = {}
    max_x = None
    max_y = None
    rand = None
    original_state = {}
    
    def _clean_board(self):
        for tile in self.board.keys():
            if self.board[tile] in [7, 8]:
                self.board[tile] = 6
    
    def _validity_enforced(self):
        zeroes = get_all(self.board, [0])
        lights = []
        for z in zeroes:
            neighbors = get_neighbors(self, z[0], z[1])
            for n in neighbors:
                if self.board[n] == 6:
                    self.board[n] = -1
            
        num_boxes = get_all(self.board, [1, 2, 3, 4])
        for box in num_boxes:
            if get_neighbor_values(self, box[0], box[1]).count(6) == self.board[box]:  # if there are exactly n blank
                neighbors = get_neighbors(self, box[0], box[1])                        # spaces next to the n-numbered
                for n in neighbors:                                                    # box, place light bulbs there
                    if self.board[n] == 6:
                        lights = lights + [n]
                        
        for n in self.board.keys():
            if self.board[n] == -1:
                self.board[n] = 6
                
        for l in lights:
            place_light(self, l[0], l[1])
                    
    def _random_board_create(self):
        first = self.rand.choice(get_all_unlit(self.board))  # get one random unlit tile from board
        place_light(self, first[0], first[1])  # this ensures the all boards generated have at least 1 bulb to be placed
    
        while True:  # random blank black box placement
            block_tile = self.rand.choice(get_all(self.board, [6, 7]))
            if self.rand.random() > 0.7:
                update_tile(self.board, block_tile[0], block_tile[1], 5)
            if self.rand.random() > 0.8:
                break
    
        # after the placement of black boxes, the board is updated to make sure
        # the first bulb is shining on the correct tiles (doesn't go past new black boxes)
        for m in get_all(self.board, [7, 8]):
            update_tile(self.board, m[0], m[1], 6)
        place_light(self, first[0], first[1])
    
        while True:
            unlit = get_all_unlit(self.board)
            if not len(unlit):
                break
            tile = self.rand.choice(unlit)  # gets all unlit squares
            choice = self.rand.random()
            if choice < 0.01:  # small chance to place a bulb on board
                place_light(self, tile[0], tile[1])
            elif choice > 0.98:  # smaller chance to place a blank black box
                update_tile(self.board, tile[0], tile[1], 5)

        for box in get_all(self.board, [5]):
            count = 0
            neighbors = get_neighbors(self, box[0], box[1])
            for n in neighbors:
                if self.board[n] == 8:
                    count += 1
            if self.rand.random() > 0.5:
                self.board[box] = count
            
            self._clean_board()
            self.original_state[tile] = self.board[tile]
    
        lup = str(g.seed) + '.lup'
        g.soln_file = str(g.seed) + '.soln'
        f = open(lup, 'w')
        f.write(str(g.x) + '\n')
        f.write(str(g.y) + '\n')
        for box in get_all(self.board, range(6)):
            f.write(str(box[0]) + ' ' + str(box[1]) + ' ' + str(self.board[box]) + '\n')
        f.close()
        g.filename = lup

    def refresh(self):
        for tile in self.board.keys():
            self.board[tile] = self.original_state[tile]
            
    def new_random_board(self):
        for tile in self.board.keys():
            self.board[tile] = 6
        self._random_board_create()
    
    def __init__(self):
        self.max_x = g.x
        self.max_y = g.y
        self.rand = Random(g.seed)
        
        for i in range(1, self.max_x+1):
                for j in range(1, self.max_y+1):
                    self.board[(i, j)] = 6  # sets all tiles to unlit
        
        if not g.datafile:
            self._random_board_create()
        else:
            for i in g.block_list:
                self.board[(i[0], i[1])] = i[2]
            
        if g.init_type == 'vf':             # if validity is forced, the original game board will have the
            self._validity_enforced()  # light bulbs that surround the numbered boxes in only one way already there

        for tile in self.board.keys():
            self.original_state[tile] = self.board[tile]