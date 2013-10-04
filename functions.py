__author__ = 'Chuck'
from get_boxes import *


def place_light(game, x, y):
    board = game.board
    
    if x > game.max_x or x < 1 or y > game.max_y or y < 1:
        return
    
    n = board[(x, y)]
    if n not in [6, 7]:  # there is a block or a light already occupying this spot, or cannot be placed
        return
    else:
        update_tile(board, x, y, n+2)  # n=6 -> tile is now 8 (lit): n=7 -> tile is now 9 (mutually lit)
         
    tiles = get_reachable(game, x, y)
    for t in tiles:              # lights all reachable tiles
        if board[t] in [6, -1]:  # empty tiles
            board[t] = 7         # are now lit
        elif board[t] == 8:      # light bulb tiles
            board[t] = 9         # are now lit by another light bulb


# checks to see if there are more lights surrounding a numbered black box than the number on the box
def black_box_check(game):
    boxes = get_all_num_boxes(game.board)
    for m in boxes:
        neighbors = get_neighbor_values(game, m[0], m[1])
        count = 0
        for n in neighbors:
            if n in [8, 9]:
                count += 1
        if game.board[m] < count:
            return True
    return False


# updates a tile during board creation. used for black boxes
# and by place_light.  use place_light to accurately update board
def update_tile(board, x, y, n):
    if type(n) == int:
        board[(x, y)] = n
    else:
        print 'you tried to update a tile with something that\'s not an int, idiot.'


def new_child(game, parents, enforce):
    game.refresh()
    bulbs = get_all_lights(parents[0][0]) + get_all_lights(parents[1][0])  # makes a list of all bulbs
                                                                           # from both parents
    for b in bulbs:
        if game.original_state[b] == 8:  # if the list contains validity enforced bulbs,
            bulbs.remove(b)              # remove them
            
    while True:
        try:
            b = game.rand.choice(bulbs)  # get a bulb, any bulb
        except IndexError:  # if you don't have any bulbs:
            b = (game.rand.randint(1, game.max_x), game.rand.randint(1, game.max_y))  # whatever, just get a tile

        c = game.rand.randint(1, 20)  # arbitrary, can be adjusted to change mutation rates
        if c == 1:  # chance to remove selected bulb
            try:
                bulbs.remove(b)
            except ValueError:  # if bulb-to-be-removed is a random tile and not actually a bulb:
                pass            # nothing happens
        elif c == 2:  # place light on random tile
            rand_x = game.rand.randint(1, game.max_x)
            rand_y = game.rand.randint(1, game.max_y)
            place_light(game, rand_x, rand_y)
        elif c == 3:  # breaks out of the loop, recombination over
            break
        else:  # highest probability of happening, places light on board
            mut_x = b[0] + game.rand.choice([-1, 0, 0, 0, 0, 0, 1])  # chance to skew x or y
            mut_y = b[1] + game.rand.choice([-1, 0, 0, 0, 0, 0, 1])  # by one in either direction
            place_light(game, mut_x, mut_y)                          # if bulb is placed out of bounds, nothing happens

    if len(get_all_mutually_lit(game.board)) > 0:
        return game.board, 0
    elif enforce and black_box_check(game):
        return game.board, 0
    else:
        fitness = len(get_all_lit(game.board))
        return game.board, fitness


def find_average(survivors):
    total_fitness = 0
    for s in survivors:
        total_fitness += s[1]
    return float(total_fitness)/float(len(survivors))


def find_best(survivors):
    best_fitness = (None, 0)
    for s in survivors:
        if s[1] > best_fitness[1]:
            best_fitness = s
    return best_fitness