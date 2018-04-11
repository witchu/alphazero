import numpy as np

BOARD_SIZE = 8
UNIT_TYPE = 4
INPUT_LAYER = UNIT_TYPE + 1
POS_SIZE = (BOARD_SIZE ** 2) // 2
KEY_SIZE = POS_SIZE ** 2

V2C = {
     0: '.',
     1: 'x',
     2: 'X',
    -1: 'o',
    -2: 'O',
}

KEY_ROT180 = [(BOARD_SIZE - y - 1) * BOARD_SIZE + (BOARD_SIZE - x - 1) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)]

def get_start_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE))
    for i in range(BOARD_SIZE // 2):
        board[0][i * 2    ] = +1
        board[1][i * 2 + 1] = +1
        board[BOARD_SIZE - 2][i * 2    ] = -1
        board[BOARD_SIZE - 1][i * 2 + 1] = -1
    return board

def clone_board(board):
    return np.copy(board)

def path_to_key(path, player):
    if player > 0:
        return (path[0] // 2) * POS_SIZE + (path[1] // 2)
    else:
        return (KEY_ROT180[path[0]] // 2) * POS_SIZE + (KEY_ROT180[path[1]] // 2)

def get_next_state(board, player):
    result = []
    is_pawn = (lambda v: v == 1) if player > 0 else (lambda v: v == -1)
    is_king = (lambda v: v == 2) if player > 0 else (lambda v: v == -2)
    try_pawn_jump = _try_pawn_x_jump if player > 0 else _try_pawn_o_jump
    is_enemy = (lambda v: v < 0) if player > 0 else (lambda v: v > 0)
    # try jump
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if is_pawn(v):
                try_pawn_jump(board, x, y, result)
            elif is_king(v):
                _try_king_jump(board, x, y, is_enemy, result)
    if len(result) > 0: return result
    # move
    try_pawn_move = _try_pawn_x_move if player > 0 else _try_pawn_o_move
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if is_pawn(v):
                try_pawn_move(board, x, y, result)
            elif is_king(v):
                _try_king_move(board, x, y, result)
    return result

def _try_king_jump(board, x, y, is_enemy, result, path = None):
    j0 = _can_king_jump(board, x, y, -1, -1, is_enemy)
    j1 = _can_king_jump(board, x, y, -1, +1, is_enemy)
    j2 = _can_king_jump(board, x, y, +1, -1, is_enemy)
    j3 = _can_king_jump(board, x, y, +1, +1, is_enemy)
    if j0 == 0 and j1 == 0 and j2 == 0 and j3 == 0:
        if path != None:
            result.append((path, board, True))
        return
    if path == None: path = [y * BOARD_SIZE + x]
    if j0 > 0:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, -1, -1, j0)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_king_jump(nb, nx, ny, is_enemy, result, branch)
    if j1 > 0:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, -1, +1, j1)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_king_jump(nb, nx, ny, is_enemy, result, branch)
    if j2 > 0:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, +1, -1, j2)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_king_jump(nb, nx, ny, is_enemy, result, branch)
    if j3 > 0:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, +1, +1, j3)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_king_jump(nb, nx, ny, is_enemy, result, branch)


def _try_pawn_x_jump(board, x, y, result, path = None):
    jump_left = _can_pawn_x_jump_left(board, x, y)
    jump_right = _can_pawn_x_jump_right(board, x, y)
    if not jump_left and not jump_right:
        if path != None:
            if y == BOARD_SIZE - 1: board[y][x] = +2 # promote
            result.append((path, board, True))
        return
    if path == None: path = [y * BOARD_SIZE + x]
    if jump_left:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, -1, +1, 2)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_pawn_x_jump(nb, nx, ny, result, branch)
    if jump_right:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, +1, +1, 2)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_pawn_x_jump(nb, nx, ny, result, branch)

def _try_pawn_o_jump(board, x, y, result, path = None):
    jump_left = _can_pawn_o_jump_left(board, x, y)
    jump_right = _can_pawn_o_jump_right(board, x, y)
    if not jump_left and not jump_right:
        if path != None:
            if y == 0: board[y][x] = -2 # promote
            result.append((path, board, True))
        return
    if path == None: path = [y * BOARD_SIZE + x]
    if jump_left:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, -1, -1, 2)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_pawn_o_jump(nb, nx, ny, result, branch)
    if jump_right:
        nb = clone_board(board)
        nx, ny = _jump(nb, x, y, +1, -1, 2)
        branch = path + [ny * BOARD_SIZE + nx]
        _try_pawn_o_jump(nb, nx, ny, result, branch)

def _try_king_move(board, x, y, result):
    m0 = _can_king_move(board, x, y, -1, -1)
    m1 = _can_king_move(board, x, y, -1, +1)
    m2 = _can_king_move(board, x, y, +1, -1)
    m3 = _can_king_move(board, x, y, +1, +1)
    if m0 == 0 and m1 == 0 and m2 == 0 and m3 == 0:
        return
    path = [y * BOARD_SIZE + x]
    if m0 > 0:
        for d in range(m0):
            nb = clone_board(board)
            nx, ny = _move(nb, x, y, -1, -1, d + 1)
            result.append((path + [ny * BOARD_SIZE + nx], nb, False))
    if m1 > 0:
        for d in range(m1):
            nb = clone_board(board)
            nx, ny = _move(nb, x, y, -1, +1, d + 1)
            result.append((path + [ny * BOARD_SIZE + nx], nb, False))
    if m2 > 0:
        for d in range(m2):
            nb = clone_board(board)
            nx, ny = _move(nb, x, y, +1, -1, d + 1)
            result.append((path + [ny * BOARD_SIZE + nx], nb, False))
    if m3 > 0:
        for d in range(m3):
            nb = clone_board(board)
            nx, ny = _move(nb, x, y, +1, +1, d + 1)
            result.append((path + [ny * BOARD_SIZE + nx], nb, False))

def _try_pawn_x_move(board, x, y, result):
    path = [y * BOARD_SIZE + x]
    if _can_pawn_x_move_left(board, x, y):
        nb = clone_board(board)
        nx, ny = _move(nb, x, y, -1, +1, 1)
        if ny == BOARD_SIZE - 1: nb[ny][nx] = +2 # promote
        result.append((path + [ny * BOARD_SIZE + nx], nb, True))
    if _can_pawn_x_move_right(board, x, y):
        nb = clone_board(board)
        nx, ny = _move(nb, x, y, +1, +1, 1)
        if ny == BOARD_SIZE - 1: nb[ny][nx] = +2 # promote
        result.append((path + [ny * BOARD_SIZE + nx], nb, True))

def _try_pawn_o_move(board, x, y, result):
    path = [y * BOARD_SIZE + x]
    if _can_pawn_o_move_left(board, x, y):
        nb = clone_board(board)
        nx, ny = _move(nb, x, y, -1, -1, 1)
        if ny == 0: nb[ny][nx] = -2 # promote
        result.append((path + [ny * BOARD_SIZE + nx], nb, True))
    if _can_pawn_o_move_right(board, x, y):
        nb = clone_board(board)
        nx, ny = _move(nb, x, y, +1, -1, 1)
        if ny == 0: nb[ny][nx] = -2 # promote
        result.append((path + [ny * BOARD_SIZE + nx], nb, True))
    return False

def _jump(board, x, y, mx, my, d):
    me = board[y][x]
    c = d - 1
    tx = x + mx * d
    ty = y + my * d
    board[y + my * c][x + mx * c] = 0
    board[ty][tx] = me
    board[y][x] = 0
    return tx, ty

def _move(board, x, y, mx, my, d):
    me = board[y][x]
    tx = x + mx * d
    ty = y + my * d
    board[ty][tx] = me
    board[y][x] = 0
    return tx, ty

def _can_king_jump(board, x, y, mx, my, is_enemy):
    for c in range(BOARD_SIZE - 2):
        x += mx
        y += my
        if x < 1 or y < 1 or x >= BOARD_SIZE - 1 or  y >= BOARD_SIZE - 1: return 0
        v = board[y][x]
        if v == 0: continue
        if is_enemy(v):
            if board[y + my][x + mx] == 0:
                return c + 2
        return 0
    return 0

def _can_king_move(board, x, y, mx, my):
    for c in range(BOARD_SIZE - 1):
        x += mx
        y += my
        if x < 0 or y < 0 or x >= BOARD_SIZE or  y >= BOARD_SIZE: return c
        v = board[y][x]
        if v == 0: continue
        return c
    return BOARD_SIZE - 1

def _can_pawn_x_jump_left(board, x, y):
    if x < 2 or y >= BOARD_SIZE - 2: return False
    return board[y + 1][x - 1] < 0 and board[y + 2][x - 2] == 0
    
def _can_pawn_x_jump_right(board, x, y):
    if x >= BOARD_SIZE - 2 or y >= BOARD_SIZE - 2: return False
    return board[y + 1][x + 1] < 0 and board[y + 2][x + 2] == 0

def _can_pawn_x_move_left(board, x, y):
    if x < 1: return False
    return board[y + 1][x - 1] == 0

def _can_pawn_x_move_right(board, x, y):
    if x >= BOARD_SIZE - 1: return False
    return board[y + 1][x + 1] == 0

def _can_pawn_o_jump_left(board, x, y):
    if x < 2 or y < 2: return False
    return board[y - 1][x - 1] > 0 and board[y - 2][x - 2] == 0
    
def _can_pawn_o_jump_right(board, x, y):
    if x >= BOARD_SIZE - 2 or y < 2: return False
    return board[y - 1][x + 1] > 0 and board[y - 2][x + 2] == 0

def _can_pawn_o_move_left(board, x, y):
    if x < 1: return False
    return board[y - 1][x - 1] == 0

def _can_pawn_o_move_right(board, x, y):
    if x >= BOARD_SIZE - 1: return False
    return board[y - 1][x + 1] == 0

def _can_king_play(board, x, y, is_enemy):
    if _can_king_move(board, x, y, -1, -1) > 0: return True
    if _can_king_move(board, x, y, -1, +1) > 0: return True
    if _can_king_move(board, x, y, +1, -1) > 0: return True
    if _can_king_move(board, x, y, +1, +1) > 0: return True
    if _can_king_jump(board, x, y, -1, -1, is_enemy) > 0: return True
    if _can_king_jump(board, x, y, -1, +1, is_enemy) > 0: return True
    if _can_king_jump(board, x, y, +1, -1, is_enemy) > 0: return True
    if _can_king_jump(board, x, y, +1, +1, is_enemy) > 0: return True
    return False


def _can_pawn_x_play(board, x, y):
    return _can_pawn_x_jump_left(board, x, y) or _can_pawn_x_jump_right(board, x, y) or _can_pawn_x_move_left(board, x, y) or _can_pawn_x_move_right(board, x, y)

def _can_pawn_o_play(board, x, y):
    return _can_pawn_o_jump_left(board, x, y) or _can_pawn_o_jump_right(board, x, y) or _can_pawn_o_move_left(board, x, y) or _can_pawn_o_move_right(board, x, y)

def get_winner(board, player):
    xc = 0
    oc = 0
    x_end = True
    o_end = True
    is_enemy_of_x = lambda v: v < 0
    is_enemy_of_o = lambda v: v > 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if v == +1:
                if x_end and _can_pawn_x_play(board, x, y): x_end = False
                xc += 1
            elif v == -1:
                if o_end and _can_pawn_o_play(board, x, y): o_end = False
                oc += 1
            elif v == +2:
                if x_end and _can_king_play(board, x, y, is_enemy_of_x): x_end = False
                xc += 1
            elif v == -2:
                if o_end and _can_king_play(board, x, y, is_enemy_of_o): o_end = False
                oc += 1
    if xc == 0: return -1
    if oc == 0: return +1
    if player > 0 and x_end: return -1
    if player < 0 and o_end: return +1
    return None

def get_end_score(board):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if v == +1:
                score += 1000
            elif v == -1:
                score -= 1000
            elif v == +2:
                score += 1100
            elif v == -2:
                score -= 1100
    return score

KING_POSITION = np.array([
    [-2, 0, 0, 0, 0, 0,+2, 0],
    [ 0, 0, 0, 0, 0,+1, 0,+2],
    [ 0, 0, 0, 0,+1, 0,+1, 0],
    [ 0, 0, 0,+1, 0,+1, 0, 0],
    [ 0, 0,+1, 0,+1, 0, 0, 0],
    [ 0,+1, 0,+1, 0, 0, 0, 0],
    [+2, 0,+1, 0, 0, 0, 0, 0],
    [ 0,+2, 0, 0, 0, 0, 0,-2],
], dtype=int)

def get_move_score(board):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if v == +1:
                score += 1000 + y * 10
            elif v == -1:
                score -= 1000 + (BOARD_SIZE - y - 1) * 10
            elif v == +2:
                score += 1100 + KING_POSITION[y][x]
            elif v == -2:
                score -= 1100 + KING_POSITION[y][x]
    return score

def get_heuristic_score(board):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            v = board[y][x]
            if v == +1:
                score += 1000
            elif v == -1:
                score -= 1000
            elif v == +2:
                score += 1100
            elif v == -2:
                score -= 1100
    return score

def to_string(board):
    header = '  |' + ''.join(['{}'.format(x + 1) for x in range(BOARD_SIZE)]) + '\n' + '--+' + ('-' * BOARD_SIZE) + '\n'
    return header + '\n'.join(['{:2}|'.format(y + 1) + _to_line(board, y) for y in range(BOARD_SIZE)])

def _to_line(board, y):
    b = board[y]
    m = y % 2
    return ''.join([_to_char(b[x], x, m) for x in range(BOARD_SIZE)])

def _to_char(v, x, m):
    if x % 2 != m: return ' '
    assert(v in V2C)
    return V2C[v]

def to_oneline(board):
    return ''.join([_to_line_half(board, y) for y in range(BOARD_SIZE)])

def _to_line_half(board, y):
    b = board[y]
    m = y % 2
    return ''.join([V2C[b[x * 2 + m]] for x in range(BOARD_SIZE // 2)])