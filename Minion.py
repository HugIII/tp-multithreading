import QueueManager


class Minion(QueueManager.QueueClient):
    def __init__(self):
        super().__init__()

    def get(self):
        t = self.task_queue.get()
        x = t.work()
        print("J'ai fini une tache")
        self.result_queue.put(x)


if __name__ == "__main__":
    minion = Minion()
    while 1:
        minion.get()
