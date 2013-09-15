__author__ = 'Chuck'
from get_boxes import *

def place_light(game, x, y):
    board = game.board
    n = board[(x, y)]
    if n in [0, 1, 2, 3, 4, 5, 8, 9]: #there is a block or a light already occupying this spot
        return
    else:
        update_tile(board, x, y, n+2) #n=6 -> tile is now 8 (lit): n=7 -> tile is now 9 (mutually lit)
         
    tiles = get_reachable(game, x, y)
    for t in tiles: #lights all reachable tiles 
        if board[t] == 6: #empty tiles
            board[t] = 7 #are now lit
            continue
        elif board[t] == 8: #light bulb tiles
            board[t] = 9 #are now lit by another light bulb

#checks to see if there are more lights surrounding a numbered black box than the number on the box
def black_box_check(game):
    boxes = get_all_num_boxes(game.board)
    for m in boxes:
        neighbors = get_neighbor_values(game, m[0], m[1])
        count = 0
        for n in neighbors:
            if n in [8,9]:
                count += 1
        if game.board[m] < count:
            return True
    return False

def update_tile(board, x, y, n):
    if type(n) == int:
        board[(x, y)] = n
    else:
        print 'you tried to update a tile with not an int, idiot.'