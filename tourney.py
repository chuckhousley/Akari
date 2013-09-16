from sys import maxint

def fitness_prop_select(game, survivors):
    select = []
    parents = []
    for n in range(len(survivors)): #for every index in the survivor list,
        for m in range(survivors[n][1]+1):#add fitness+1 (in case of fitness = 0) of that index to selection list
            select.append(n)
            
    parents.append(survivors[game.rand.choice(select)])#only 2 parents, arbitrary choice
    parents.append(survivors[game.rand.choice(select)])
    return parents


def parent_ktournament(game, survivors):
    parents = []
    parents.append(game.rand.choice(survivors))
    parents.append(game.rand.choice(survivors))
    return parents

def survivor_ktournament(game, survivors, mu):
    return game.rand.sample(survivors, mu)

def survivor_truncation(game, survivors, mu):
    while len(survivors) > mu:
        worst_fitness = maxint
        worst_survivor = None
        for n in range(len(survivors)):
            if survivors[n][1] <= worst_fitness:
                worst_fitness = survivors[n][1]
                worst_survivor = n
        del survivors[worst_survivor]
    return survivors