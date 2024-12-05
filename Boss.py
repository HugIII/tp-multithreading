import manager
from task import Task


class Boss(manager.QueueClient):
    def __init__(self):
        super().__init__()
        self.te = 0

    def post(self):
        # size = np.random.randint(300, 3_000)
        # a = np.random.rand(size, size)
        # b = np.random.rand(size)
        t = Task(size=600)
        self.task_queue.put(t)

    def get(self):
        re = self.result_queue.get()
        print("J'ai reçu un résultat " + str(re.x))
        print("J'ai mis " + str(re.time))
        self.te += re.time
        print("Temps total" + str(self.te))


if __name__ == "__main__":
    boss = Boss()
    for i in range(10):
        boss.post()

    print("J'ai fini de post les tâches.")

    while 1:
        boss.get()
