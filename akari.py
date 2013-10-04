__author__ = 'Chuck'

from Game import Game
import g
from functions import get_all_lights, new_child, calculate_penalty_fitness, place_light
from tourney import *
from log_fn import *
from search import evolution
from random import Random, randint
from get_boxes import get_all_lights
import sys


def main():
    #theres a better way to do this, but this is faster
    fn = sys.argv[2] if (len(sys.argv) == 3 and sys.argv[1] == '-c') else 'default.cfg'
        
    g.init(fn)     # read in the input file to the project's globals
    game = Game()  # create the initial game board
    log = open(g.logfile, 'w')
    prepare_log(log)
    
    best_fitness = -maxint
    best_soln = None

    for n in range(g.runs):
        print 'Starting run #' + str(n+1) + '\n'
        log.write('Run ' + str(n+1) + '\n')
        result = evolution(game, log)
        
        if result[1] > best_fitness:
            best_soln = list(get_all_lights(result[0]))
            best_fitness = int(result[1])
        if n < g.runs-1 and not g.datafile:
            log.close()
            create_soln_file(best_fitness, best_soln)
            g.seed = randint(0, maxint)
            game.rand = Random(g.seed)
            game.new_random_board()
            log = open(g.logfile, 'w')
            prepare_log(log)

    log.close()
    print 'finished calculations'
    create_soln_file(best_fitness, best_soln)


if __name__ == '__main__':
    main()
