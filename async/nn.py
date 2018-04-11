import asyncio
from asyncio.futures import Future

class NN:
    def __init__(self, nn, bulk_size):
        self.nn = nn
        self.tasks = []
        self.bulk_size = bulk_size

    def predict(self, x):
        future = Future()
        self.tasks.append((x, future))
        if (len(self.tasks) >= self.bulk_size):
            self._flush()
        return future

    def _flush(self):
        ts = self.tasks
        self.tasks = []
        X = [x for x, future in ts]
        F = [future for x, future in ts]
        P, V = self.nn.bulkPredict(X)
        for i in range(len(X)):
            F[i].set_result((P[i], V[i][0]))
