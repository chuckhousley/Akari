__author__ = 'Chuck'

from Game import *
from Input import *
from functions import get_all_lights, random_board_create
from search import random_search
import sys


def main():
    #theres a better way to do this, but this is faster
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        filename = sys.argv[2]
    else:
        filename = 'default.cfg'

    file_input = Input(filename)
    game = Game(file_input)

    if not file_input.datafile:
        random_board_create(game, file_input)

    best_result = -1
    best_soln = None

    log = open(file_input.logfile, 'w')
    prepare_log(log, file_input)

    soln = open(file_input.solnfile, 'w')

    for m in range(file_input.runs):
        log.write('\nRun ' + str(m+1) + '\n')
        for n in xrange(10000):
            result = random_search(game, file_input.black_box)
            log.write(str(n+1) + '\t' + str(result) + '\n')
            if result > best_result:
                best_result = result
                best_soln = get_all_lights(game.board)
            game.refresh()

    log.close()

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