__author__ = 'Chuck'


def get_all_unlit(board):
    unlit = []
    for tile in board.keys():
        if board[tile] == 6:
            unlit.append(tile)
    return unlit


def get_all_lit(board):
    lit = []
    for tile in board.keys():
        if board[tile] in [7, 8]:
            lit.append(tile)
    return lit


def get_all_mutually_lit(board):
    mutlit = []
    for tile in board.keys():
        if board[tile] == 9:
            mutlit.append(tile)
    return mutlit


def update_tile(board, x, y, n):
    board[(x, y)] = n


def get_neighbors(board, x, y):
    neighbors = []
    if x > 1:
        neighbors.append((x-1, y))
    if x < board.max_x:
        neighbors.append((x+1, y))
    if y > 1:
        neighbors.append((x, y-1))
    if y < board.max_y:
        neighbors.append((x, y+1))
    return neighbors


def rec_lightable_tile_finder(game, x, y):
    if x < 1 or y < 1 or x > game.max_x or y > game.max_y:
        return False
    if game.board[(x, y)] in [0, 1, 2, 3, 4, 5, 9]:
        return False
    if game.board[(x, y)] in [6, 7, 8]:
        return True


def get_reachable(game, x, y):
    reachable = []
    for i in range(1, game.max_x):
        if not rec_lightable_tile_finder(game, x+i, y):
            break
        else:
            reachable.append((x+i, y))

    for i in range(1, game.max_x):
        if not rec_lightable_tile_finder(game, x-i, y):
            break
        else:
            reachable.append((x-i, y))

    for i in range(1, game.max_y):
        if not rec_lightable_tile_finder(game, x, y+i):
            break
        else:
            reachable.append((x, y+i))
    for i in range(1, game.max_y):
        if not rec_lightable_tile_finder(game, x, y-i):
            break
        else:
            reachable.append((x, y-i))
    return reachable


def get_lights(board):
    lights = []
    for tile in board.keys():
        if board[tile] == 7:
            lights.append(tile)
    return lights


def place_light(game, x, y):
    board = game.board
    n = board[(x, y)]
    if n in [0, 1, 2, 3, 4, 5, 8, 9]:
        return
    else:
        update_tile(board, x, y, n+2)
    tiles = get_reachable(game, x, y)
    for t in tiles:
        if board[t] == 6:
            board[t] = 7
            continue
        elif board[t] == 7:
            board[t] = 9