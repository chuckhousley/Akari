__author__ = 'Chuck'

from Game import Game
import globals
from functions import get_all_lights, new_child
from tourney import *
from search import evolution
from random import Random, randint
import sys

def main():
    print 'start'
    #theres a better way to do this, but this is faster
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        fn = sys.argv[2]
    else:
        fn = 'default.cfg'
        
    globals.init(fn)    # read in the input file to the project's globals
    game = Game()       # create the initial game board
    
    log = open(globals.logfile, 'w')
    prepare_log(log)
    
    best_fitness = -1
    best_soln = None

    sys.exit()

    for n in range(globals.runs):
        print 'Starting run #' + str(n+1) + '\n'
        log.write('\nRun ' + str(n+1) + '\n')
        result = evolution(game, pg, log)
        
        if result[1] >= best_fitness:
            best_board = result[0]
            best_soln = get_all_lights(result[0])
            best_fitness = result[1]
        if not globals.datafile:
            globals.seed = randint(0, maxint)
            game.rand = Random(globals.seed)
            game.new_random_board(pg)
    #################################
    log.close()

    soln = open(globals.solnfile, 'w')
    soln.write(str(best_fitness) + '\n')
    for coordinates in best_soln:
        soln.write(str(coordinates[0]) + ' ' + str(coordinates[1]) + '\n')
    soln.close()


def prepare_log(log):
    log.write('Result Log\n')
    log.write('Datafile: ' + globals.filename + '\n')
    log.write('Seed: ' + str(globals.seed) + '\n')
    log.write('Black box enforcement: ' + ('True\n' if globals.black_box == 1 else 'False\n'))


if __name__ == '__main__':
    main()