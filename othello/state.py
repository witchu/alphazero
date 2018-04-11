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
        return util.BOARD_SIZE_2 + 1

    def getRepresentativeString(self):
        return ('x|' if self.currentPlayer > 0 else 'o|') + util.to_oneline(self.board)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getWinner(self):
        return self.winner

    def getAction(self):
        assert(self.winner == None)
        result = []
        player = self.currentPlayer
        another = player * -1
        for i in range(util.BOARD_SIZE_2):
            if self.board[i] == 0 and util.can_place_at(self.board, i, i % util.BOARD_SIZE, player, another):
                result.append((i, i)) # (action, key)
        if len(result) == 0:
            # skip
            result.append((util.BOARD_SIZE_2, util.BOARD_SIZE_2))
        return result

    def actionToString(self, action):
        y = action // util.BOARD_SIZE + 1
        x = action %  util.BOARD_SIZE + 1
        return str(x) + str(y)

    def getNextState(self, action):
        assert(self.winner == None)
        state = State(self)
        if action == util.BOARD_SIZE_2:
            state.currentPlayer *= -1
        else:
            player = self.currentPlayer
            another = player * -1
            util.place_at(state.board, action, action % util.BOARD_SIZE, player, another)
            state.currentPlayer = another
            state.winner = util.get_winner(state.board)
        return state

    def reorderAction(self, action_list):
        pass

    def getEndScore(self):
        return util.get_end_score(self.board)

    def getHeuristicScore(self):
        return util.get_heuristic_score(self.board)

    def getNnInput(self):
        board = self.board
        inp = np.zeros((2, util.BOARD_SIZE, util.BOARD_SIZE))
        x = inp[0 if self.currentPlayer > 0 else 1]
        o = inp[1 if self.currentPlayer > 0 else 0]
        i1 = 0
        i2 = 0
        for i in range(util.BOARD_SIZE_2):
            if board[i] > 0:
                x[i1][i2] = 1
            elif board[i] < 0:
                o[i1][i2] = 1
            i2 += 1
            if i2 >= util.BOARD_SIZE:
                i1 += 1
                i2 = 0
        return inp

    def __str__(self):
        return util.to_string(self.board)

    def __repr__(self):
        return util.to_string(self.board)
