__author__ = 'Chuck'
import random
from sys import maxint


def you_messed_up():
        print "Invalid input. Please check command line arguments, .cfg,  and .lup files for errors"
        exit()


def init(fn):
    global datafile
    global filename
    global logfile
    global soln_file
    global mu
    global lam  # lambda
    global runs
    global evaluations
    global init_type
    global parent_select
    global survivor_select
    global k_parent
    global k_survive
    global strategy
    global penalty
    global light_penalty
    global box_penalty
    global terminate
    global x
    global y
    global seed
    global black_box
    global block_list

    datafile = None
    filename = None
    logfile = None
    soln_file = None
    mu = None
    lam = None  # lambda
    runs = None
    evaluations = None
    init_type = None
    parent_select = None
    survivor_select = None
    k_parent = None
    k_survive = None
    strategy = None
    penalty = None
    light_penalty = None
    box_penalty = None
    terminate = None
    x = None
    y = None
    seed = None
    black_box = None
    block_list = []

    filename = fn
    try:
        f = open(filename, 'r')
    except IOError:
        print 'failed to open', filename
        you_messed_up()
    
    for line in f:
        if line[:8] == 'datafile':
            try:
                datafile = int(line[9])
            except ValueError:
                print 'datafile\n'
                you_messed_up()
        elif line[:8] == 'filename':
            try:
                filename = line[9:-1]
            except ValueError:
                filename = None
        elif line[:6] == 'size_x':
            try:
                x = int(line[7:])
            except ValueError:
                x = 1
        elif line[:6] == 'size_y':
            try:
                y = int(line[7:])
            except ValueError:
                y = 1
        elif line[:4] == 'seed':
            try:
                seed = int(line[5:])
            except ValueError:
                seed = 0
        elif line[:4] == 'runs':
            try:
                runs = int(line[5:])
            except ValueError:
                print 'runs\n'
                you_messed_up()
        elif line[:4] == 'eval':
            try:
                evaluations = int(line[5:])
            except ValueError:
                print 'eval\n'
                you_messed_up()
        elif line[:4] == 'init':
            try:
                init_type = line[5:-1]
            except ValueError:
                print 'init\n'
                you_messed_up()
        elif line[:6] == 'parent':
            try:
                parent_select = line[7:-1]
            except ValueError:
                print 'parent\n'
                you_messed_up()
        elif line[:8] == 'survivor':
            try:
                survivor_select = line[9:-1]
            except ValueError:
                print 'survivor\n'
                you_messed_up()
        elif line[:2] == 'mu':
            try:
                mu = int(line[3:])
            except ValueError:
                print 'mu\n'
                you_messed_up()
        elif line[:6] == 'lambda':
            try:
                lam = int(line[7:])
            except ValueError:
                print 'lambda\n'
                you_messed_up()
        elif line[:7] == 'kparent':
            try:
                k_parent = int(line[8:])
            except ValueError:
                print 'kparent\n'
                you_messed_up()
        elif line[:9] == 'ksurvival':
            try:
                k_survive = int(line[10:])
            except ValueError:
                print 'ksurvival\n'
                you_messed_up()
        elif line[:8] == 'strategy':
            try:
                strategy = line[9:-1]
            except ValueError:
                print 'strategy\n'
                you_messed_up()
        elif line[:9] == 'terminate':
            try:
                terminate = int(line[10:])
            except ValueError:
                you_messed_up()
        elif line[:7] == 'logfile':
            try:
                logfile = line[8:-1]
            except ValueError:
                you_messed_up()
        elif line[:8] == 'solnfile':
            try:
                soln_file = line[9:-1]
            except ValueError:
                you_messed_up()
    f.close()
    
    if datafile == 1:
        try:
            f = open(filename, 'r')
        except IOError:
            you_messed_up()
        try:
            x = int(f.readline())
            y = int(f.readline())
        except ValueError:
            you_messed_up()
        for line in f:
            r = line.split(' ')
            block_list.append((int(r[0]), int(r[1]), int(r[2])))
        f.close()
    
    if not seed:
        seed = random.randint(0, maxint)
    if mu > evaluations or lam > evaluations:
        print 'Too few evaluations. Either increase evaluations or reduce mu and lambda'
        exit()