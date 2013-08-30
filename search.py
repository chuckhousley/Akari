__author__ = 'Chuck'
from functions import *


def random_search(b):
    tiles = get_all_unlit(b.board)
    for t in tiles:
        if b.rand.random() > 0.5:
            update_tile(b.board, t[0], t[1], 8)
    tiles2 = get_all_unlit(b.board)

    print len(tiles)
    print len(tiles2)