BOARD_SIZE = 8
BOARD_SIZE_2 = BOARD_SIZE * BOARD_SIZE

def get_start_board():
    board = [0 for x in range(BOARD_SIZE_2)]
    pos0 = BOARD_SIZE_2 // 2 - BOARD_SIZE // 2 - 1
    board[pos0] = -1
    board[pos0 + 1] = +1
    board[pos0 + BOARD_SIZE] = +1
    board[pos0 + BOARD_SIZE + 1] = -1
    return board

def clone_board(board):
    return [board[x] for x in range(BOARD_SIZE_2)]

def next_board(board, at, player, another):
    if board[at] != 0: return None
    x = at % BOARD_SIZE
    if not can_place_at(board, at, x, player, another):
        return None
    nb = clone_board(board)
    place_at(nb, at, x, player, another)
    return nb


def can_place_at(board, at, x, player, another):
    if _can_place(board, at, -BOARD_SIZE, BOARD_SIZE, player, another) > 0: return True
    if _can_place(board, at, +BOARD_SIZE, BOARD_SIZE, player, another) > 0: return True
    if x >= 2:
        if _can_place(board, at, -BOARD_SIZE - 1, x - 1, player, another) > 0: return True
        if _can_place(board, at, -1, x - 1, player, another) > 0: return True
        if _can_place(board, at, +BOARD_SIZE - 1, x - 1, player, another) > 0: return True
    rb = BOARD_SIZE - 2
    if x < rb:
        if _can_place(board, at, -BOARD_SIZE + 1, rb - x, player, another) > 0: return True
        if _can_place(board, at, +1, rb - x, player, another) > 0: return True
        if _can_place(board, at, +BOARD_SIZE + 1, rb - x, player, another) > 0: return True
    return False

def _can_place(board, at, diff, loop, player, another):
    at += diff
    if at < 0: return 0
    if at >= BOARD_SIZE_2: return 0
    if board[at] != another: return 0
    for mx in range(loop):
        at += diff
        if at < 0: return 0
        if at >= BOARD_SIZE_2: return 0
        v = board[at]
        if v == 0: return 0
        if v == player: return mx + 1
    return 0

def place_at(board, at, x, player, another):
    _try_place(board, at, -BOARD_SIZE, BOARD_SIZE, player, another)
    _try_place(board, at, +BOARD_SIZE, BOARD_SIZE, player, another)
    if x >= 2:
        _try_place(board, at, -BOARD_SIZE - 1, x - 1, player, another)
        _try_place(board, at, -1, x - 1, player, another)
        _try_place(board, at, +BOARD_SIZE - 1, x - 1, player, another)
    rb = BOARD_SIZE - 2
    if x < rb:
        _try_place(board, at, -BOARD_SIZE + 1, rb - x, player, another)
        _try_place(board, at, +1, rb - x, player, another)
        _try_place(board, at, +BOARD_SIZE + 1, rb - x, player, another)
        
def _try_place(board, at, diff, loop, player, another):
    n = _can_place(board, at, diff, loop, player, another)
    if n == 0: return
    board[at] = player
    for mx in range(n):
        at += diff
        board[at] = player

def to_string(board):
    header = '  |' + ''.join(['{}'.format(x + 1) for x in range(BOARD_SIZE)]) + '\n' + '--+' + ('-' * BOARD_SIZE) + '\n'
    return header + '\n'.join(['{:2}|'.format(y + 1) + _to_line(board, y) for y in range(BOARD_SIZE)])

def to_oneline(board):
    return ''.join([_to_line(board, y) for y in range(BOARD_SIZE)])

def _to_line(board, y):
    yz = y * BOARD_SIZE
    return ''.join([_to_char(board[yz + x]) for x in range(BOARD_SIZE)])

def _to_char(v):
    if v == 0: return '.'
    elif v > 0: return 'x'
    else: return 'o'

def get_winner(board):
    x = 0
    o = 0
    for at in range(BOARD_SIZE_2):
        if board[at] > 0: x += 1
        elif board[at] < 0: o += 1
    if x == 0:
        return -1
    elif o == 0:
        return +1
    elif x + o == BOARD_SIZE_2 or not _can_play(board):
        if x > o: return +1
        elif x < o: return -1
        else: return 0
    else:
        return None

def _can_play(board):
    for at in range(BOARD_SIZE_2):
        x = at % BOARD_SIZE
        if board[at] == 0 and (can_place_at(board, at, x, +1, -1) or can_place_at(board, at, x, -1, +1)):
            return True
    return False

def get_end_score(board):
    score = 0
    for at in range(BOARD_SIZE_2):
        score += board[at]
    return score

def _score(at):
    x = at %  BOARD_SIZE
    y = at // BOARD_SIZE
    if (x == 0 or x == BOARD_SIZE - 1) and  (y == 0 or y == BOARD_SIZE - 1):
       return 115
    if (x <= 1 or x >= BOARD_SIZE - 2) and (y <= 1 or y >= BOARD_SIZE - 2):
       return 95
    if (x == 0 or x == BOARD_SIZE - 1) or (y == 0 or y == BOARD_SIZE - 1):
       return 101
    return 100

HEURISTIC_SCORE = [_score(i) for i in range(BOARD_SIZE_2)]

def get_heuristic_score(board):
    score = 0
    for at in range(BOARD_SIZE_2):
        score += board[at] * HEURISTIC_SCORE[at]
    return score
    