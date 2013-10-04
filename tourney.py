from sys import maxint
import g


def fitness_prop_select(game, survivors):
    select = []
    parents = []
    for n in range(len(survivors)):         # for every index in the survivor list,
        for m in range(max(1, survivors[n][1])):  # add fitness+1 (in case of fitness = 0) of that index to selection list
            select.append(n)
            
    parents.append(survivors[game.rand.choice(select)])  # only 2 parents, arbitrary choice
    parents.append(survivors[game.rand.choice(select)])
    return parents


def parent_ktournament(game, survivors):
    return_list = []
    for f in range(g.k_parent):
        return_list += [game.rand.choice(survivors)]
    return return_list


def survivor_ktournament(game, survivors):
    return_list = []
    for f in range(g.k_survive):
        new_entry = game.rand.choice(survivors)
        if not return_list.count(new_entry):
            return_list += [new_entry]
    return return_list


def survivor_truncation(survivors):
    while len(survivors) > g.mu:
        worst_fitness = maxint
        worst_survivor = None
        for n in range(len(survivors)):
            if survivors[n][1] <= worst_fitness:
                worst_fitness = survivors[n][1]
                worst_survivor = n
        del survivors[worst_survivor]
    return survivors


def uniform_random_selection(game, selection):
    return game.rand.sample(selection, g.mu)