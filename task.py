import time

import numpy as np


class Task:
    def __init__(self, a, b, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        #self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = a
        self.b = b
        # prepare room for the results
        self.x = np.zeros((size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start
        return self.x
