import sys

import argparse
parser = argparse.ArgumentParser(description='generate game states from mcts+nn')
parser.add_argument('game', help='a game name i.e. checkers')
parser.add_argument('-m', '--model', default='latest.h5', help='model filename')
parser.add_argument('-n', '--task', default=8, type=int, help='number of coroutine tasks')
parser.add_argument('-s', '--simulation', default=100, type=int, help='number of simulations per move')
parser.add_argument('--hard', default=0, type=int, help='number of random moves')
parser.add_argument('--soft', default=30, type=int, help='number of random moves that depends on visited node count')
parser.add_argument('--progress', action='store_true', help='show progress bar')
parser.add_argument('--gpu', type=float, help='gpu memory fraction')
parser.add_argument('--file', help='save to a file')
parser.add_argument('--network', help='save to remote server')
args = parser.parse_args(sys.argv[1:])

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

from async.nn import NN as async_nn
state = State()
nn = async_nn(NN(args.model), args.task)
file = None

from tqdm import tqdm
pbar = tqdm()

import asyncio

if args.network != None:
    import requests
    loop = asyncio.get_event_loop()
    def post(url, payload):
        requests.post(url, data = payload)
    def submit(url, model, result):
        payload = { 'model': model, 'result': result }
        loop.run_in_executor(None, post, url, payload)
    def submit_to_remote_server(result):
        submit(args.network, args.model, result)
        pbar.update()
    callback = submit_to_remote_server
elif args.file != None:
    file = open(args.file, 'w')
    def save_to_file(result):
        file.write(result)
        file.write('\n')
        file.flush()
    callback = save_to_file
else:
    def print_to_stdout(result):
        print(result)
    callback = print_to_stdout

from async.generator import generate
for i in range(args.task):
    asyncio.ensure_future(generate(state, nn, callback, {
        'simulation': args.simulation,
        'hard_random': args.hard,
        'soft_random': args.soft,
    }))

loop = asyncio.get_event_loop()
loop.run_forever()
loop.close()

if file != None:
    file.close()
