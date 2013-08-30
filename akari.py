__author__ = 'Chuck'

from Board import *
from Input import *
import sys


def main():
    seed = 3
    rand = random.Random(seed)
    filename = 'default.cfg'
    input = Input(filename)

    r = Board(input)

if __name__ == '__main__':
    main()