__author__ = 'Chuck'
from functions import *
from get_boxes import *


def random_search(game, enforce):
    while True:
        chance = game.rand.random()
        count = 0
        while True:
            try:
                t = game.rand.choice(get_all_unlit(game.board))
            except IndexError:
                break
            if game.rand.random() > chance:
                #place_light(game, t[0], t[1])
                count += 1
                break
        if len(get_all_mutually_lit(game.board)) > 0 or (enforce and black_box_check(game)):
            return 0
        if game.rand.randint(0,1):
            break
    return len(get_all_lit(game.board))
