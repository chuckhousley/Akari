__author__ = 'Chuck'
import random
from sys import maxint


class Input:
    datafile = None
    filename = None
    x = None
    y = None
    seed = None
    black_box = None
    runs = None
    logfile = None
    solnfile = None
    block_list = []

    def you_messed_up(self):
        print "Invalid input. Please check .cfg and .lup files for errors"
        exit()

    def __init__(self, filename):
        try:
            f = open(filename, 'r')
        except IOError:
            self.you_messed_up()

        for line in f:
            if line[0:8] == 'datafile':
                try:
                    self.datafile = int(line[9])
                except ValueError:
                    self.you_messed_up()
            elif line[0:8] == 'filename':
                try:
                    self.filename = line[9:-1]
                except ValueError:
                    self.filename = None
            elif line[0:6] == 'size_x':
                try:
                    self.x = int(line[7:])
                except ValueError:
                    self.x = 0
            elif line[0:6] == 'size_y':
                try:
                    self.y = int(line[7:])
                except ValueError:
                    self.y = 0
            elif line[0:4] == 'seed':
                try:
                    self.seed = int(line[5:])
                except ValueError:
                    self.seed = 0
            elif line[0:9] == 'black_box':
                self.black_box = line[10:-1]  #this does something later?
            elif line[0:4] == 'runs':
                try:
                    self.runs = int(line[5:])
                except ValueError:
                    self.you_messed_up()
            elif line[0:7] == 'logfile':
                try:
                    self.logfile = line[8:-1]
                except ValueError:
                    self.you_messed_up()
            elif line[0:8] == 'solnfile':
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

        if self.seed == 0 or not self.seed:
            self.seed = random.randint(0, maxint)