__author__ = 'Chuck'


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
    return get_all(board, [7])

def update_tile(board, x, y, n):
    board[(x, y)] = n


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
        elif board[t] == 8:
            board[t] = 9


def black_box_check(game):
    boxes = get_all_num_boxes(game.board)
    for m in boxes:
        if game.board[m] != len(get_neighbors(game, m[0], m[1])):
            return False
    return True


def random_board_create(game, file_input):
    first = game.rand.choice(get_all_unlit(game.board))
    place_light(game, first[0], first[1])

    while True:
        block_tile = game.rand.choice(get_all(game.board, [6, 7]))
        if game.rand.random() > 0.7:
            update_tile(game.board, block_tile[0], block_tile[1], 5)
        if game.rand.random > 0.8:
            break

    for m in get_all(game.board, [7, 8]):
        update_tile(game.board, m[0], m[1], 6)
    place_light(game, first[0], first[1])

    while True:
        tile = game.rand.choice(get_all_unlit(game.board))
        choice = game.rand.random()
        if choice < 0.01:
            place_light(game, tile[0], tile[1])
        elif choice > 0.95:
            update_tile(game.board, tile[0], tile[1], 5)
        if not len(get_all_unlit(game.board)):
            break

    for box in get_all(game.board, [5]):
        count = 0
        neighbors = get_neighbors(game, box[0], box[1])
        for n in neighbors:
            if game.board[n] == 8:
                count += 1
        if game.rand.random() > 0.5:
            game.board[box] = count

    for tile in game.board.keys():
        if game.board[tile] in [7, 8]:
            game.board[tile] = 6
        game.original_state[tile] = game.board[tile]

    lup = 'puzzle-' + str(file_input.seed) + '.lup'
    f = open(lup, 'w')
    f.write(str(file_input.x) + '\n')
    f.write(str(file_input.y) + '\n')
    for box in get_all(game.board, range(6)):
        f.write(str(box[0]) + ' ' + str(box[1]) + ' ' + str(game.board[box]) + '\n')
    f.close()
    file_input.filename = lup

