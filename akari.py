__author__ = 'Chuck'

from Game import *
from Input import *
from search import random_search
import sys


def main():
    filename = 'default.cfg'
    input = Input(filename)
    print input.seed
    game = Game(input)

    random_search(game)
    best_result = -1

    for n in range(input.runs):
        for m in range(10000):
            result = random_search(game)
            if result > best_result:
                print result
                best_result = result
            game.refresh()


if __name__ == '__main__':
    main()