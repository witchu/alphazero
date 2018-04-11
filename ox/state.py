import numpy as np

from . import internal as util

class State:
    def __init__(self, prototype = None):
        if prototype == None:
            self.board = util.get_start_board()
            self.currentPlayer = 1
            self.winner = None
        else:
            self.board = util.clone_board(prototype.board)
            self.currentPlayer = prototype.currentPlayer
            self.winner = prototype.winner

    def getKeySize(self):
        return util.KEY_SIZE

    def getRepresentativeString(self):
        return ('x|' if self.currentPlayer > 0 else 'o|') + util.to_oneline(self.board)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getWinner(self):
        return self.winner

    def getAction(self):
        assert(self.winner == None)
        return util.get_action(self.board)

    def actionToString(self, action):
        y = action // util.BOARD_SIZE + 1
        x = action %  util.BOARD_SIZE + 1
        return str(x) + str(y)

    def getNextState(self, action):
        assert(self.winner == None)
        state = State(self)
        util.place_at(state.board, action, state.currentPlayer)
        state.currentPlayer *= -1
        state.winner = util.get_winner(state.board)
        return state

    def reorderAction(self, action_list):
        pass

    def getEndScore(self):
        # same score for every endings
        return 0

    def getHeuristicScore(self):
        # no heuristic
        return 0

    def getNnInput(self):
        board = self.board
        inp = np.zeros((2, util.BOARD_SIZE, util.BOARD_SIZE))
        x = inp[0 if self.currentPlayer > 0 else 1]
        o = inp[1 if self.currentPlayer > 0 else 0]
        for i1 in range(util.BOARD_SIZE):
            for i2 in range(util.BOARD_SIZE):
                v = board[i1][i2]
                if v > 0:
                    x[i1][i2] = 1
                elif v < 0:
                    o[i1][i2] = 1
        return inp

    def __str__(self):
        return util.to_string(self.board)

    def __repr__(self):
        return util.to_string(self.board)
