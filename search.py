__author__ = 'Chuck'
import globals
from functions import *
from get_boxes import *
from tourney import *


def random_search(game, enforce):
    game.refresh()
    while True:
        chance = game.rand.random()
        while True:
            try:
                t = game.rand.choice(get_all(game.board, [6, 7]))
            except IndexError:
                break
            if game.rand.random() < chance:
                place_light(game, t[0], t[1])
                break
        if len(get_all_mutually_lit(game.board)) > 0:
            return game.board, 0
        elif enforce and black_box_check(game):
            return game.board, 0
        elif not game.rand.randint(0, 10):
            return_board = {}
            for n in game.board.keys():
                return_board[n] = game.board[n]
            return return_board, len(get_all_lit(game.board))


def evolution(game, log):
    survivors = []
    children = []
    best = (None, 0)
    total_evals = globals.mu
    
    for m in range(globals.mu):
        game.refresh()
        new_parent = random_search(game, globals.black_box)
        survivors.append(new_parent)

    while total_evals < globals.evaluations:
        update_log(log, total_evals, survivors)
        while len(children) < globals.lam and total_evals < globals.evaluations:
            if globals.parent_select == 'fps':
                parents = fitness_prop_select(game, survivors)
            elif globals.parent_select == 'k':
                parents = parent_ktournament(game, survivors)
            else:
                parents = Null
                print('Parent selection not valid, please update the cfg file')
                exit()

            child = new_child(game, parents, globals.black_box)
            for n in child[0].keys():
                if child[0][n] == 9 and child[1] > 0:
                    print 'what'  
            children.append(child)
            total_evals += 1
            
        survivors.extend(children)
        children = []
        
        if globals.survivor_select == 't':
            survivors = survivor_truncation(game, survivors, globals.mu)
        elif globals.survivor_select == 'k':
            survivors = survivor_ktournament(game, survivors, globals.mu)
        new_best = find_best(survivors)
        if new_best[1] >= best[1]:
            best = new_best
    
    return best