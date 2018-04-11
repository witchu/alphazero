def replay(argv):
    import argparse
    parser = argparse.ArgumentParser(description='replay state')
    parser.add_argument('game', help='a game name i.e. checkers')
    parser.add_argument('history', help='state history')
    args = parser.parse_args(argv)

    from util import game
    State = game.importState(args.game).State

    history = args.history.split(' ')[1:]

    state = State()
    print(state)
    for action in history:
        print(action)
        acs = state.getAction()
        select_action = None
        for encoded_action, k in acs:
            decoded_action = state.actionToString(encoded_action)
            if action == decoded_action:
                select_action = encoded_action
                break
        assert(select_action != None)
        state = state.getNextState(select_action)
        print(state)
    assert(state.getWinner() != None)
