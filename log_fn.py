__author__ = 'Chuck'
import g
from functions import find_average, find_fronts


def prepare_log(log):
    log.write('Result Log\n')
    log.write('\nSolution file:\t' + g.soln_file + '\n')
    log.write('Runs:\t' + str(g.runs) + '\n')
    log.write('Evaluations:\t' + str(g.evaluations) + '\n')
    log.write('Mu:\t' + str(g.mu) + '\n')
    log.write('Lambda:\t' + str(g.lam) + '\n')
    log.write('Parent selection used:\t' + g.parent_select + '\n')
    log.write('Survivor selection used:\t' + g.survivor_select + '\n')
    log.write('K size for k-tournament parent selection:\t' + str(g.k_parent) + '\n')
    log.write('K size for k-tournament survivor selection:\t' + str(g.k_survive) + '\n')
    log.write('Survival Strategy:\t' + g.strategy + '\n')
    log.write('Termination limit:\t' + str(g.terminate) + '\n')
    log.write('Datafile: ' + str(g.filename) + '\n')
    log.write('Seed: ' + str(g.seed) + '\n')
    log.write('Black box enforcement: ' + ('True\n' if g.black_box == 1 else 'False\n'))
    log.write('\n==================================================\n')


def update_log(log, total_evals, survivors):
    averages = find_average(survivors)
    best_values = find_fronts(survivors)
    ret_str = str(total_evals) + '\t'
    ret_str += str('%.2f' % averages[0]) + '\t'
    ret_str += str(best_values[1]) + '\t'
    ret_str += str('%.2f' % averages[1]) + '\t'
    ret_str += str(best_values[2]) + '\t'
    ret_str += str('%.2f' % averages[2]) + '\t'
    ret_str += str(best_values[3]) + '\t'
    log.write(ret_str + '\n')


def create_soln_file(best_fitness, best_soln):
    soln = open(g.soln_file, 'w')
    soln.write(str(best_fitness) + '\n')
    for coordinates in best_soln:
        soln.write(str(coordinates[0]) + ' ' + str(coordinates[1]) + '\n')
    soln.close()
    print 'solution written'
