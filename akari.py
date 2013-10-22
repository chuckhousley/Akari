__author__ = 'Chuck'

from Game import Game
import g
from functions import get_all_lights, new_child, calculate_penalty_fitness, place_light, determine_dominance
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

    best_soln = [(None, -maxint, -maxint, -maxint)]

    for n in range(g.runs):
        print 'Starting run #' + str(n+1) + '\n'
        log.write('Run ' + str(n+1) + '\n')
        result = evolution(game, log)
        
        best_soln = determine_dominance(best_soln, result)
        if n < g.runs-1 and not g.datafile:
            create_soln_file(best_soln)
            g.seed = randint(0, maxint)
            game.rand = Random(g.seed)
            game.new_random_board()

    log.close()
    print 'finished calculations'
    create_soln_file(best_soln)


if __name__ == '__main__':
    main()
