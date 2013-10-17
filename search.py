__author__ = 'Chuck'
import g
from log_fn import *
from functions import *
from get_boxes import *
from tourney import *
from search_fn import *


def random_search(game):
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
        if not game.rand.randint(0, 10):
            return_board = {}
            fitness, subfit_light, subfit_box = calculate_penalty_fitness(game)
            for n in game.board.keys():
                return_board[n] = game.board[n]
            return return_board, fitness, subfit_light, subfit_box


def evolution(game, log):
    survivors = []
    children = []
    best_board = {}
    best_fitness = 0
    total_evals = g.mu
    
    for m in range(g.mu):  # creates initial list of mu parents
        game.refresh()     # uses uniform random search to create list
        survivors.append(random_search(game))

    while total_evals < g.evaluations:
        update_log(log, total_evals, survivors)
        del children[:]
        while len(children) < g.lam and total_evals < g.evaluations:
            parents = parent_selection(game, survivors)
            children.append(new_child(game, parents))
            total_evals += 1
            
        survivors = survivor_selection(game, survivors, children)

        new_best = find_fronts(survivors)
        if new_best[1] >= best_fitness:
            best_fitness = int(new_best[1])
            best_board = dict(new_best[0])
    return best_board, best_fitness