__author__ = 'Chuck'

from Game import Game
import g
from functions import get_all_lights, new_child
from tourney import *
from log_fn import *
from search import evolution
from random import Random, randint
import sys


def main():
    #theres a better way to do this, but this is faster
    fn = sys.argv[2] if (len(sys.argv) == 3 and sys.argv[1] == '-c') else 'default.cfg'
        
    g.init(fn)     # read in the input file to the project's globals
    game = Game()  # create the initial game board
    
    log = open(g.logfile, 'w')
    prepare_log(log)
    
    best_fitness = -1
    best_soln = None

    for n in range(g.runs):
        print 'Starting run #' + str(n+1) + '\n'
        log.write('Run ' + str(n+1) + '\n')
        result = evolution(game, log)
        
        if result[1] >= best_fitness:
            best_soln = get_all_lights(result[0])
            best_fitness = result[1]
        if not g.datafile:
            g.seed = randint(0, maxint)
            game.rand = Random(g.seed)
            game.new_random_board()

    log.close()
    create_soln_file(best_fitness, best_soln)


if __name__ == '__main__':
    main()