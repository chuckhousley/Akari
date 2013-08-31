__author__ = 'Chuck'
from functions import *


def random_search(game, enforce):
    chance = .99#game.rand.random()
    tiles = get_all_unlit(game.board)
    for t in tiles:
        if game.rand.random() > chance:
            place_light(game, t[0], t[1])
    if len(get_all_mutually_lit(game.board)) > 0 and enforce and black_box_check(game):
        return 0
    else:
        return len(get_all_lit(game.board))