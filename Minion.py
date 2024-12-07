"""
====================================================================
File: Minion.py 
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    This script defines the `Minion` class, which represents a worker 
    that fetches tasks from a shared task queue, processes them, and 
    places the results into a shared result queue.
    These queues are managed by the QueueManager class.

Usage:
    python Minion.py 

Version: 1.0.0
====================================================================
"""


import manager

# This class inherits from QueueClient, which communicates with the QueueManager
class Minion(manager.QueueClient):
    def __init__(self):
        super().__init__()

    def get(self):
        # Retrieve a task from the task queue.
        t = self.task_queue.get()
        # Perform the task's computation.
        t.work()
        print("J'ai fini la tache ", t.identifier)
        # Place the completed task into the result queue.
        self.result_queue.put(t)


if __name__ == "__main__":
    minion = Minion()
    while 1:
        minion.get()
