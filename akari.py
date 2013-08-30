__author__ = 'Chuck'

from Board import *
from Input import *
from search import random_search
import sys


def main():
    filename = 'default.cfg'
    input = Input(filename)
    r = Board(input)
    random_search(r)


if __name__ == '__main__':
    main()