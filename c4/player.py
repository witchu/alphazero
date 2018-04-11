from util.compat import compat_input
from . import internal as util

class HumanPlayer:
    def __init__(self):
        pass

    def getNextAction(self, state):
        action = state.getAction()
        available_x = []
        for i in range(len(action)):
            a, k = action[i]
            x = a %  util.BOARD_SIZE_W + 1
            y = a // util.BOARD_SIZE_W + 1
            print('{} - {},{}'.format(x, x, y))
            available_x.append(x)
        while True:
            try:
                x = int(compat_input('enter x: '))
                if x in available_x:
                    for i in range(len(action)):
                        if available_x[i] == x:
                            select = i
                            break
                    break
            except ValueError:
                pass
        a, k = action[select]
        return a
