import numpy as np

from . import internal as util

class State:
    def __init__(self, mode = None, nb = None, player = None, idle = None):
        if mode == None:
            self.board = util.get_start_board()
            self.currentPlayer = 1
            self.winner = None
            self.idle = 0
        else:
            self.board = nb
            self.currentPlayer = player
            self.winner = None
            self.idle = idle

    def getKeySize(self):
        return util.KEY_SIZE

    def getRepresentativeString(self):
        return ('x|' if self.currentPlayer > 0 else 'o|') + '{}|'.format(self.idle) + util.to_oneline(self.board)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getWinner(self):
        return self.winner

    def getAction(self):
        assert(self.winner == None)
        # ((path, board, advance), key)
        return [(r, util.path_to_key(r[0], self.currentPlayer)) for r in util.get_next_state(self.board, self.currentPlayer)]

    def actionToString(self, action):
        (path, board, advance) = action
        return '-'.join(str(v % util.BOARD_SIZE + 1) + str(v // util.BOARD_SIZE + 1) for v in path)

    def getNextState(self, action):
        assert(self.winner == None)
        board = action[1]
        advance = action[2]
        idle = 0 if advance else (self.idle + 1)
        state = State("clone", board, self.currentPlayer * -1, idle)
        state.winner = util.get_winner(state.board, state.currentPlayer) if state.idle < 16 else 0
        return state

    def reorderAction(self, action_list):
        #action_list.sort(key=lambda v: -v[0][2])
        def score(v):
            return util.get_move_score(v[0][1])
        action_list.sort(key=score, reverse=self.currentPlayer>0)

    def getEndScore(self):
        return 0#util.get_end_score(self.board)

    def getHeuristicScore(self):
        return util.get_heuristic_score(self.board)

    def getNnInput(self):
        inp = np.zeros((util.INPUT_LAYER, util.BOARD_SIZE, util.BOARD_SIZE))
        if self.currentPlayer > 0:
            pawn_x = 0
            pawn_o = 2
            king_x = 1
            king_o = 3
        else:
            pawn_x = 2
            pawn_o = 0
            king_x = 3
            king_o = 1
        for y in range(util.BOARD_SIZE):
            for x in range(util.BOARD_SIZE):
                v = self.board[y][x]
                if v == +1:
                    inp[pawn_x][y][x] = 1
                elif v == -1:
                    inp[pawn_o][y][x] = 1
                elif v == +2:
                    inp[king_x][y][x] = 1
                elif v == -2:
                    inp[king_o][y][x] = 1
        if self.idle > 0:
            inp[4][:] = self.idle
        if self.currentPlayer < 0:
            return np.rot90(inp, 2, (1, 2))
        return inp

    def __str__(self):
        return util.to_string(self.board)

    def __repr__(self):
        return util.to_string(self.board)
