import numpy as np

from .minimax import Minimax
from .mcts import MCTS
from .compat import compat_input

def newPlayer(game, settings):
    from .game import importNn, importPlayer

    settings = settings.split(',')
    t = settings[0]
    if t == 'random':
        return RandomPlayer()
    elif t == 'minimax':
        depth = int(settings[1]) if len(settings) >= 2 else 6
        return MinimaxPlayer(depth)
    elif t == 'policy':
        nn = importNn(game).NN(settings[1])
        return PolicyPlayer(nn)
    elif t == 'mcts':
        nn = importNn(game).NN(settings[1])
        sim_count = int(settings[2]) if len(settings) >= 3 else 100
        return MctsPlayer(nn, sim_count)
    else:
        return importPlayer(game).HumanPlayer()

class RandomPlayer:
    def __init__(self):
        pass

    def prepare(self):
        pass

    def getNextAction(self, state):
        action = state.getAction()
        index = np.random.choice(len(action))
        a, k = action[index]
        return a

class SimplePlayer:
    def __init__(self):
        pass

    def prepare(self):
        pass

    def getNextAction(self, state):
        action = state.getAction()
        a, k = action[0]
        return a

class MinimaxPlayer:
    def __init__(self, depth, verbose=True):
        self.minimax = Minimax(depth)
        self.verbose = verbose

    def prepare(self):
        pass

    def getNextAction(self, state):
        return self.minimax.getBestAction(state,  self.verbose)

class PolicyPlayer:
    def __init__(self, nn, verbose=True):
        self.nn = nn
        self.verbose = verbose

    def prepare(self):
        pass

    def getNextAction(self, state):
        action = state.getAction() # (action, key)
        raw_policy, value = self.nn.predict(state.getNnInput())
        best_policy = -1
        best_action = None
        if self.verbose:
            print('value = {}'.format(value))
        for i in range(len(action)):
            a, k = action[i]
            policy = raw_policy[k]
            if self.verbose:
                print('{:2} - {:0.6f} {}'.format(i + 1, policy, state.actionToString(a)))
            if policy > best_policy:
                best_policy = policy
                best_action = a
        return best_action

class MctsPlayer:
    def __init__(self, nn, sim_count, verbose=True):
        self.mcts = MCTS(nn)
        self.sim_count = sim_count
        self.verbose = verbose

    def prepare(self):
        self.mcts.resetStats()

    def getNextAction(self, state):
        return self.mcts.getMostVisitedAction(state, self.sim_count, self.verbose)

class HumanPlayer:
    def __init__(self):
        pass

    def prepare(self):
        pass

    def getNextAction(self, state):
        action = state.getAction()
        for i in range(len(action)):
            a, k = action[i]
            print('{:2} - {}'.format(i, state.actionToString(a)))
        while True:
            try:
                select = int(compat_input('select action: '))
                if 0 <= select and select < len(action): break
            except ValueError:
                pass
        a, k = action[select]
        return a
