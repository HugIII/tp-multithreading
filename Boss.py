"""
====================================================================
File: Boss.py
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    Master script. This script create task and send them to the QueueManager.

Usage:
    python Boss.py

Local dependencies:
        - manager (manager.py)
        - task (task.py)

Version: 1.0.0
====================================================================
"""

import manager
from task import Task


# This class inherits from QueueClient, which communicates with the QueueManager
class Boss(manager.QueueClient):
    def __init__(self):
        super().__init__()
        # Cumulative resolution times for each task
        self.te = 0

    def post(self):
        # create and send task to queue
        for i in range(10):
            # create task
            t = Task(identifier=i, size=3000)
            self.task_queue.put(t)
            print("ajout de la tache " + str(i) + " dans la liste.")

    def get(self):
        # get solved taks in the result queue
        re = self.result_queue.get()

        # print the result of the solved task
        print("La tache " + str(re.identifier) + " donne le résultat : " + str(re.x))
        # print the time of the solved task
        print("J'ai mis " + str(re.time))

        # calculation and print of the cumulative time
        self.te += re.time
        print("Temps total : " + str(self.te))


if __name__ == "__main__":
    # create Boss instance and post the task
    boss = Boss()
    boss.post()

    # debug print end of post
    print("J'ai fini de post les tâches.")

    while 1:
        # wait solved task
        boss.get()
