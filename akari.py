__author__ = 'Chuck'

from Game import Game
from Input import Input #for project globals
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
        
    pg = Input(fn) #read in the input file to the project's globals class
    game = Game(pg) #create the initial game board
    
    log = open(pg.logfile, 'w')
    prepare_log(log, pg)
    
    best_fitness = -1
    best_soln = None
    
    for n in range(pg.runs):
        print 'Starting run #' + str(n+1) + '\n'
        log.write('\nRun ' + str(n+1) + '\n')
        result = evolution(game, pg, log)
        
        if result[1] >= best_fitness:
            best_soln = get_all_lights(result[0])
            best_fitness = result[1]
        if not pg.datafile:
            pg.seed = randint(0, maxint)
            game.rand = Random(pg.seed)
            game.new_random_board(pg)    
        
    
    #################################
    log.close()

    
    
    '''for m in range(pg.runs):
        log.write('\nRun ' + str(m+1) + '\n')
        print 'Running Run #' + str(m+1) + '\n'
        for n in xrange(pg.evaluations):
            result = random_search(game, pg.black_box)
            if result > best_result:
                log.write(str(n+1) + '\t' + str(result) + '\n')
                best_result = result
                best_soln = get_all_lights(game.board)
            game.refresh()'''
    soln = open(pg.solnfile, 'w')
    soln.write(str(best_fitness) + '\n')
    for coordinates in best_soln:
        soln.write(str(coordinates[0]) + ' ' + str(coordinates[1]) + '\n')
    soln.close()


def prepare_log(log, file_input):
    log.write('Result Log\n')
    log.write('Datafile: ' + file_input.filename + '\n')
    log.write('Seed: ' + str(file_input.seed) + '\n')
    log.write('Black box enforcement: ' + ('True\n' if file_input.black_box == 1 else 'False\n'))


if __name__ == '__main__':
    main()