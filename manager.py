"""
====================================================================
File: manager.py
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    This script defines a QueueManager to manage shared queues for
    tasks and results in a multiprocessing environment. It also
    provides a QueueClient class for clients, Boss and Minion, to connect to the manager.

Usage:
    python manager.py

Version: 1.0.0
====================================================================
"""

from multiprocessing.managers import BaseManager
from queue import Queue


# Custom manager class to manage task and result queues
class QueueManager(BaseManager):
    def __init__(self):
        # Initialize the manager with a network address and authentication key
        super().__init__(address=("127.0.0.1", 50000), authkey=b"abc")
        self.task_queue = Queue()  # Queue for pending tasks
        self.result_queue = Queue()  # Queue for completed tasks
        # Register the shared queues with callable methods
        super().register("task", callable=lambda: self.task_queue)
        super().register("result", callable=lambda: self.result_queue)


# Client class to connect to the QueueManager
class QueueClient:
    def __init__(self):
        # Initialize a connection to the manager
        self.m = QueueManager()
        self.m.connect()  # Connect to the QueueManager server

        # Register and retrieve the task queue
        self.m.register("task")
        self.task_queue = self.m.task()

        # Register and retrieve the result queue
        self.m.register("result")
        self.result_queue = self.m.result()


if __name__ == "__main__":
    m = QueueManager()
    m.start()
    while 1:
        pass
