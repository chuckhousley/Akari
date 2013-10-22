__author__ = 'Chuck'
from get_boxes import *
import g
from sys import maxint


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

    return_value = 0
    for m in boxes:
        neighbors = get_neighbor_values(game, m[0], m[1])
        count = 0
        for n in neighbors:
            if n in [8, 9]:
                count += 1
        return_value += count - game.board[(m[0], m[1])] if count > game.board[(m[0], m[1])] else 0

    return return_value


# updates a tile during board creation. used for black boxes
# and by place_light.  use place_light to accurately update board
def update_tile(board, x, y, n):
    if type(n) == int:
        board[(x, y)] = n
    else:
        print 'you tried to update a tile with something that\'s not an int, idiot.'


def calculate_penalty_fitness(game):
    fitness = len(get_all_lit(game.board))
    light_penalty = -1 * len(get_all_mutually_lit(game.board))
    box_penalty = -1 * black_box_check(game)
    return fitness, light_penalty, box_penalty


def calculate_normal_fitness(game):
    if len(get_all_mutually_lit(game.board)) > 0:
        return 0
    elif g.black_box and not black_box_check(game):
        return 0
    else:
        return len(get_all_lit(game.board))


def remove_bulb_from_list(bulbs, current):
    try:
        bulbs.remove(current)
    except ValueError:  # if bulb-to-be-removed is a random tile and not actually a bulb:
        pass            # nothing happens


def new_child(game, parents):
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
            remove_bulb_from_list(bulbs, b)
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
            remove_bulb_from_list(bulbs, b)

    fitness, subfit_light, subfit_box = calculate_penalty_fitness(game)
    return dict(game.board), fitness, subfit_light, subfit_box


def find_average(survivors):
    total_fitness = 0
    subfit_light = 0
    subfit_box = 0
    for s in survivors:
        total_fitness += s[1]
        subfit_light += s[2]
        subfit_box += s[3]
    fitness = float(total_fitness)/float(len(survivors))
    light = float(subfit_light)/float(len(survivors))
    box = float(subfit_box)/float(len(survivors))
    return fitness, light, box


def find_fronts(survivors):
    fronts = [[]]  # begins by creating an empty pareto front
    for s in survivors:  # loops through all survivors
        if not len(fronts[0]):
            fronts[0].append(s)  # adds first survivor to pareto front
        else:
            added = False
            allowed = True
            dominated = []
            for a in range(len(fronts)):  # checks to see if the current survivor has
                for b in fronts[a]:       # same fitness as member in current front
                    cond_fit = s[1] == b[1]    # a duplicate fitness would imply that the
                    cond_light = s[2] == b[2]  # survivor would belong on the same front
                    cond_box = s[3] == b[3]
                    if cond_fit and cond_light and cond_box:
                        fronts[a].append(s)
                        added = True
                        break

                if not added:            # if the survivor was not added that way:
                    for b in fronts[a]:  # checks to see if the survivor is dominating
                        cond_fit = s[1] >= b[1]    # a member of the current front
                        cond_light = s[2] >= b[2]  # if so, then the survivor is added to
                        cond_box = s[3] >= b[3]    # the front and the dominated members are pushed down
                        if cond_fit and cond_light and cond_box:
                            dominated.append(b)
                    if len(dominated):
                        for d in dominated:
                            fronts[a].remove(d)        # the dominated elements are removed from their level
                        fronts.insert(a+1, dominated)  # and are placed on a new level below the old one
                        fronts[a].append(s)            # the survivor is inserted to level above the dominated elements
                        added = True
                        break

                if not added:            # if the survivor still hasn't been added, checks to see if
                    for b in fronts[a]:  # it can be placed on an existing level due to nondominance
                        cond_fit = s[1] < b[1]    # if the survivor has fitness levels strictly less than
                        cond_light = s[2] < b[2]  # a member of the current level, then the survivor
                        cond_box = s[3] < b[3]    # cannot join the level
                        if cond_fit and cond_light and cond_box:
                            allowed = False
                            break

                if allowed and not added:  # if the survivor was not already added to the
                    fronts[a].append(s)    # front but is allowed due to nondominance
                    added = True           # then it is added
                    break
            if added:
                continue

            else:  # if all else fails, then the survivor's fitness levels were too low
                fronts.append([s])  # and a new level is created for it.

    return list(fronts)


def determine_dominance(old, new):
    for a in old:
        for b in new:
            if a[1] < b[1] and a[2] < b[2] and a[3] < b[3]:
                return new
    return old


def find_best(survivors):
    best_fit = best_light = best_box = -maxint
    for n in survivors:
        best_fit = n[1] if n[1] > best_fit else best_fit
        best_light = n[2] if n[2] > best_light else best_light
        best_box = n[3] if n[3] > best_box else best_box
    return best_fit, best_light, best_box