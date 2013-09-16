__author__ = 'Chuck'
import random
from sys import maxint


class Input:

    datafile = None
    filename = None
    logfile = None
    solnfile = None
    mu = None
    lam  = None #lambda
    runs = None
    evaluations = None
    init = None
    parent_select = None
    survivor_select = None
    kparent = None
    ksurvive = None
    terminate = None
    x = None
    y = None
    seed = None
    black_box = None
    block_list = []
    
    
    def you_messed_up(self):
        print "Invalid input. Please check command line arguments, .cfg,  and .lup files for errors"
        exit()
    
    def __init__(self, fn):
        self.filename = fn
        try:
            f = open(self.filename, 'r')
        except IOError:
            self.you_messed_up()
        
        for line in f:
            if line[:8] == 'datafile':
                try:
                    self.datafile = int(line[9])
                except ValueError:
                    self.you_messed_up()
            elif line[:8] == 'filename':
                try:
                    self.filename = line[9:-1]
                except ValueError:
                    self.filename = None
            elif line[:6] == 'size_x':
                try:
                    self.x = int(line[7:])
                except ValueError:
                    self.x = 1
            elif line[:6] == 'size_y':
                try:
                    self.y = int(line[7:])
                except ValueError:
                    self.y = 1
            elif line[:4] == 'seed':
                try:
                    self.seed = int(line[5:])
                except ValueError:
                    self.seed = 0
            elif line[:9] == 'black_box':
                try:
                    self.black_box = int(line[10])
                except ValueError:
                    self.you_messed_up()
            elif line[:4] == 'runs':
                try:
                    self.runs = int(line[5:])
                except ValueError:
                    self.you_messed_up()
            elif line[:4] == 'eval':
                try:
                    self.evaluations = int(line[5:])
                except ValueError:
                    self.you_messed_up()
            elif line[:4] == 'init':
                try:
                    self.init = line[5:-1]
                except ValueError:
                    self.you_messed_up()
            elif line[:6] == 'parent':
                try:
                    self.parent_select = line[7:-1]
                except ValueError:
                    self.you_messed_up()
            elif line[:8] == 'survivor':
                try:
                    self.survivor_select = line[9:-1]
                except ValueError:
                    self.you_messed_up()
            elif line[:2] == 'mu':
                try:
                    self.mu = int(line[3:])
                except ValueError:
                    self.you_messed_up()
            elif line [:6] == 'lambda':
                try:
                    self.lam = int(line[7:])
                except ValueError:
                    self.you_messed_up()
            elif line[:7] == 'kparent':
                try:
                    self.kparent = int(line[8:])
                except ValueError:
                    self.you_messed_up()
            elif line[:9] == 'ksurvival':
                try:
                    self.ksurvive = int(line[10:])
                except ValueError:
                    self.you_messed_up()
            elif line[:9] == 'terminate':
                try:
                    self.terminate = int(line[10:])
                except ValueError:
                    self.you_messed_up()
            elif line[:7] == 'logfile':
                try:
                    self.logfile = line[8:-1]
                except ValueError:
                    self.you_messed_up()
            elif line[:8] == 'solnfile':
                try:
                    self.solnfile = line[9:-1]
                except ValueError:
                    self.you_messed_up()
        f.close()
        
        if self.datafile == 1:
            try:
                f = open(self.filename, 'r')
            except IOError:
                self.you_messed_up()
            try:
                self.x = int(f.readline())
                self.y = int(f.readline())
            except ValueError:
                self.you_messed_up()
            for line in f:
                r = line.split(' ')
                self.block_list.append((int(r[0]), int(r[1]), int(r[2])))
            f.close()
        
        if not self.seed:
            self.seed = random.randint(0, maxint)