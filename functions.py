__author__ = 'Chuck'


def get_all_unlit(board):
    unlit = []
    for tile in board.keys():
        if board[tile] == 6:
            unlit.append(tile)
    return unlit


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


def rec_light(board, x, y):
    if x < 1 or y < 1 or x > board.max_x or y > board.max_y:
        return False
    if board[(x, y)] in [0, 1, 2, 3, 4, 5, 9]:
        return False
    if board[(x, y)] in [6, 7, 8]:
        return True


def get_reachable(board, x, y):
    reachable = []
    for i in range(1, board.max_x):
        if not rec_light(board, x+i, y):
            break
        else:
            reachable.append((x+i, y))

    for i in range(1, board.max_x):
        if not rec_light(board, x-i, y):
            break
        else:
            reachable.append((x-i, y))

    for i in range(1, board.max_y):
        if not rec_light(board, x, y+i):
            break
        else:
            reachable.append((x, y+i))
    for i in range(1, board.max_y):
        if not rec_light(board, x, y-i):
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


def place_light(board, x, y):
    n = board[(x, y)]
    if n in [0, 1, 2, 3, 4, 5, 8, 9]:
        return
    else:
        update_tile(board, x, y, n+2)
    tiles = get_reachable(board, x, y)
    for t in tiles:
        if board[t] == 6:
            board[t] = 7
        elif board[t] == 8:
            board[t] = 9
        else:
            continue