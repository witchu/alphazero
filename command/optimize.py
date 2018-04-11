def optimize(argv):
    import argparse
    parser = argparse.ArgumentParser(description='optimize end-game state')
    parser.add_argument('game', help='a game name i.e. checkers')
    parser.add_argument('player', default='minimax,6', nargs='?', help='optimized by which player')
    parser.add_argument('history', nargs='?', help='history from command-line')
    parser.add_argument('--truncate', default=18, type=int, help='truncate last N actions')
    parser.add_argument('--file', nargs=2, help='file names to load/save history')
    parser.add_argument('--network', help='remote server url to load/save history')
    parser.add_argument('--reoptimize', action='store_true', help='re-optimize not successful optimize states')
    parser.add_argument('--verbose', action='store_true', help='show optimized actions')
    args = parser.parse_args(argv)

    from util import game
    State = game.importState(args.game).State
    state = State()

    from util.player import newPlayer
    player = newPlayer(args.game, args.player)

    from util import optimizer

    if args.history != None:
        player.prepare()
        history = prepare_history(args.history, args)
        result = optimizer.optimize(state, history, player, args.verbose)
        print(result)
        return
    
    if args.file != None:
        with open(args.file[1], 'w') as outfile:
            with open(args.file[0], 'r') as infile:
                for line in infile:
                    player.prepare()
                    history = prepare_history(line, args)
                    result = optimizer.optimize(state, history, player, args.verbose)
                    outfile.write(result)
                    outfile.write('\n')
                    outfile.flush()
        return

    if args.network != None:
        from util import server
        get = args.network + ('reoptimize.php' if args.reoptimize else 'unoptimize.php')
        put = args.network + 'optimize.php'
        while True:
            result = server.getUnoptimize(get)
            if result == None: break
            (model, unoptimized_history) = result
            player.prepare()
            history = prepare_history(unoptimized_history, args)
            result = optimizer.optimize(state, history, player, args.verbose)
            server.optimize(put, model, unoptimized_history, result)
        return

def prepare_history(history, args):
    return history.split(' ')[1:-args.truncate]
