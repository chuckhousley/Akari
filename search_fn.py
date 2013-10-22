__author__ = 'Chuck'
import g
from tourney import *


def parent_selection(game, survivors):
    if g.parent_select == 'fps':
        return fitness_prop_select(game, survivors)
    elif g.parent_select == 'k':
        return parent_ktournament(game, survivors)
    elif g.parent_select == 'ur':
        return uniform_random_selection(game, survivors)
    else:
        print 'Invalid parent selection, please update the cfg file'
        exit(1)


def _survivor_select(game, survivors):
    if g.survivor_select == 't':
        return survivor_truncation(survivors)
    elif g.survivor_select == 'k':
        return survivor_ktournament(game, survivors)
    elif g.survivor_select == 'fps':
        return fitness_prop_select(game, survivors)
    elif g.survivor_select == 'ur':
        return uniform_random_selection(game, survivors)
    else:
        print 'Invalid survivor selection, please update the cfg file'
        exit(1)


def survivor_selection(game, survivors, children):
    if g.strategy == 'plus':
        return list(_survivor_select(game, list(survivors + children)))
    elif g.strategy == 'comma':
        return list(_survivor_select(game, list(children)))
    else:
        print 'Invalid selection strategy, please update the cfg file'
        exit(1)