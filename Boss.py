import manager
from task import Task


class Boss(manager.QueueClient):
    def __init__(self):
        super().__init__()
        self.te = 0

    def post(self):
        for i in range(10):
            t = Task(identifier=i,size=3000)
            self.task_queue.put(t)
            print("ajout de la tache " + str(i) + " dans la liste.")

    def get(self):
        re = self.result_queue.get()
        print("La tache " + str(re.identifier) + " donne le résultat : " + str(re.x))
        print("J'ai mis " + str(re.time))
        self.te += re.time
        print("Temps total : " + str(self.te))


if __name__ == "__main__":
    boss = Boss()
    boss.post()

    print("J'ai fini de post les tâches.")

    while 1:
        boss.get()
