def loop(argv):
    import argparse
    parser = argparse.ArgumentParser(description='loop generate and train')
    parser.add_argument('game', help='a game name i.e. checkers')
    parser.add_argument('begin', default=1, type=int, help='begin with generation number')
    parser.add_argument('count', nargs='?', default=100, type=int, help='number of generation')
    parser.add_argument('-n', '--number', default=10000, type=int, help='number of generated states')
    parser.add_argument('-s', '--simulation', default=100, type=int, help='number of simulations per move')
    parser.add_argument('--hard', default=0, type=int, help='number of random moves')
    parser.add_argument('--soft', default=1000, type=int, help='number of random moves that depends on visited node count')
    parser.add_argument('--epoch', default=1, type=int, help='training epochs')
    parser.add_argument('--batch', default=256, type=int, help='batch size')
    parser.add_argument('--block', default=100000, type=int, help='block size')
    parser.add_argument('--gpu', type=float, help='gpu memory fraction')
    args = parser.parse_args(argv)

    # set gpu memory
    if args.gpu != None:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session

        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = args.gpu
        set_session(tf.Session(config=config))

    from util import game
    State = game.importState(args.game).State
    NN = game.importNn(args.game).NN

    state = State()
    state_no = args.begin
    nn = NN('{:06}.h5'.format(state_no))

    for i in range(args.count):
        history_filename = '{:06}.txt'.format(state_no)
        # generate
        with open(history_filename, 'a') as file:
            def save_to_file(result):
                file.write(result)
                file.write('\n')
                file.flush()
            callback = save_to_file
            from util.generator import generate
            generate(state, nn, callback, {
                'selfplay': args.number,
                'simulation': args.simulation,
                'hard_random': args.hard,
                'soft_random': args.soft,
                'progress': True,
            })
        # train
        for epoch in range(args.epoch):
            from util.trainer import train
            train(state, nn, history_filename, {
                'batch': args.batch,
                'block': args.block,
                'progress': True,
            })
        # next generation
        state_no += 1
        nn.save('{:06}.h5'.format(state_no))
