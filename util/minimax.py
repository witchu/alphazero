big = 10000000
very_big = 1000000000

class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.transposition = {}

    def getBestAction(self, state, verbose=False):
        start_depth = self.depth - 1
        player = state.getCurrentPlayer()
        action = state.getAction()
        state.reorderAction(action)
        best_score = -very_big
        best_action = None
        alpha = -very_big + 1
        for a, k in action:
            ns = state.getNextState(a)
            #nh = ns.getRepresentativeString()
            nh = None
            score = -self._minimax(ns, nh, start_depth, -very_big, -alpha, -player)
            if verbose: print(state.actionToString(a), score)
            if score > best_score:
                best_score = score
                best_action = a
            if score > alpha:
                alpha = score
        return best_action

    def _minimax(self, state, h, depth, alpha, beta, player):
        assert(player == state.getCurrentPlayer())
        winner = state.getWinner()
        if (winner != None):
            return ((big + 100000 * depth) * winner + state.getEndScore()) * player
        if depth <= 0:
            return state.getHeuristicScore() * player

        action = state.getAction()
        #state.reorderAction(action)
        best_score = -very_big
        for a, k in action:
            ns = state.getNextState(a)
            #nh = ns.getRepresentativeString()
            nh = None
            score = -self._minimax(ns, nh, depth - 1, -beta, -alpha, -player)
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break

        return best_score
