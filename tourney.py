from sys import maxint
import g
from functions import find_fronts


def fitness_prop_select(game, survivors):
    select = []
    parents = []
    fronts = find_fronts(survivors)

    for m in range(len(fronts)):
        for n in fronts[m]:
            for p in range(len(fronts)-m+1):
                select.append(n)

    parents.append(game.rand.choice(select))  # only 2 parents, arbitrary choice
    parents.append(game.rand.choice(select))
    return parents


def parent_ktournament(game, survivors):
    return_list = []
    tourney_list = []
    while len(return_list) < g.mu:
        del tourney_list[:]
        for f in range(g.k_parent):
            tourney_list += [game.rand.choice(survivors)]
        fronts = find_fronts(tourney_list)
        return_list.append(game.rand.choice(fronts[0]))
    return return_list


def survivor_ktournament(game, survivors):
    return_list = []
    tourney_list = []
    while len(return_list) < g.mu:
        del tourney_list[:]
        for f in range(g.k_survive):
            new_entry = game.rand.choice(survivors)
            if not tourney_list.count(new_entry):
                tourney_list += [new_entry]
        fronts = find_fronts(tourney_list)
        return_list.append(game.rand.choice(fronts[0]))
    return return_list


def survivor_truncation(survivors):
    fronts = find_fronts(survivors)
    survivors_sorted = []
    for f in fronts:
        for d in f:
            survivors_sorted.append(d)
    del survivors_sorted[g.mu:]
    return survivors_sorted


def uniform_random_selection(game, selection):
    return game.rand.sample(selection, g.mu)