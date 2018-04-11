import numpy as np

BOARD_SIZE = 3
KEY_SIZE = BOARD_SIZE * BOARD_SIZE

CHECK_LIST = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]

def get_start_board():
    return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int8)

def clone_board(board):
    return np.copy(board)

def get_action(board):
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                p = y * BOARD_SIZE + x
                # (action, key)
                result.append((p, p))
    return result

def place_at(board, p, player):
    x = p %  BOARD_SIZE
    y = p // BOARD_SIZE
    board[y][x] = player

def get_winner(board):
    for c in CHECK_LIST:
        v0 = board[c[0][0]][c[0][1]]
        if v0 == 0: continue
        v1 = board[c[1][0]][c[1][1]]
        if v0 != v1: continue
        v2 = board[c[2][0]][c[2][1]]
        if v1 != v2: continue
        return v0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                return None
    return 0

def to_string(board):
    header = '  |' + ''.join(['{}'.format(x + 1) for x in range(BOARD_SIZE)]) + '\n' + '--+' + ('-' * BOARD_SIZE) + '\n'
    return header + '\n'.join(['{:2}|'.format(y + 1) + _to_line(board, y) for y in range(BOARD_SIZE)])

def to_oneline(board):
    return ''.join([_to_line(board, y) for y in range(BOARD_SIZE)])

def _to_line(board, y):
    b = board[y]
    return ''.join([_to_char(b[x]) for x in range(BOARD_SIZE)])

def _to_char(v):
    if v > 0: return 'x'
    if v < 0: return 'o'
    return '.'
