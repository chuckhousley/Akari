__author__ = 'Chuck'

from Game import Game
from Input import Input #for project globals
from functions import get_all_lights, new_child
from tourney import *
from search import random_search
import sys

def main():
    #theres a better way to do this, but this is faster
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        fn = sys.argv[2]
    else:
        fn = 'default.cfg'
        
    pg = Input(fn) #read in the input file to the project's globals class
    game = Game(pg) #create the initial game board
    survivors = []
    children = []
    
    '''for m in range(pg.mu):
        new_parent = random_search(game, pg.black_box)
        survivors.append((game.board, new_parent))
        game.refresh()
    while len(children) < pg.lam:
        if pg.parent_select == 'fps':
            parents = fitness_prop_select(game, survivors)
        elif pg.parent_select == 'k':
            parents = parent_ktournament(game, survivors)
            
        children.append(new_child(game, parents))'''
            
        
    best_result = -1
    best_soln = None

    log = open(pg.logfile, 'w')
    prepare_log(log, pg)
    for m in range(pg.runs):
        log.write('\nRun ' + str(m+1) + '\n')
        print 'Running Run #' + str(m+1) + '\n'
        for n in xrange(pg.evaluations):
            result = random_search(game, pg.black_box)
            if result > best_result:
                log.write(str(n+1) + '\t' + str(result) + '\n')
                best_result = result
                best_soln = get_all_lights(game.board)
            game.refresh()
    log.close()
    
    soln = open(pg.solnfile, 'w')
    soln.write(str(best_result) + '\n')
    for coordinates in best_soln:
        soln.write(str(coordinates[0]) + ' ' + str(coordinates[1]) + '\n')
    soln.close()


def prepare_log(log, file_input):
    log.write('Result Log\n')
    log.write('Datafile: ' + file_input.filename + '\n')
    log.write('Seed: ' + str(file_input.seed) + '\n')
    log.write('Black box enforcement: ' + 'True\n' if file_input.black_box == 1 else 'False\n')


if __name__ == '__main__':
    main()