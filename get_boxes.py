def get_all(board, n):
    return_list = []
    for tile in board.keys():
        if board[tile] in n:
            return_list.append(tile)
    return return_list


def get_all_num_boxes(board):
    return get_all(board, range(5))


def get_all_unlit(board):
    return get_all(board, [6])


def get_all_lit(board):
    return get_all(board, [7, 8])


def get_all_mutually_lit(board):
    return get_all(board, [9])


def get_all_lights(board):
    return get_all(board, [8, 9])

def get_neighbors(game, x, y):
    neighbors = []
    if x > 1:
        neighbors.append((x-1, y))
    if x < game.max_x:
        neighbors.append((x+1, y))
    if y > 1:
        neighbors.append((x, y-1))
    if y < game.max_y:
        neighbors.append((x, y+1))
    return neighbors

def get_neighbor_values(game, x, y):
    neighbors = get_neighbors(game, x, y)
    values = []
    for n in neighbors:
        values.append(game.board[n])
    return values

def rec_lightable_tile_finder(game, x, y):
    if x < 1 or y < 1 or x > game.max_x or y > game.max_y:
        return False
    if game.board[(x, y)] in [0, 1, 2, 3, 4, 5, 9]:
        return False
    if game.board[(x, y)] in [-1, 6, 7, 8]:
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