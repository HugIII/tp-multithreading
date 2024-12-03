import QueueManager
import numpy as np
from task import Task

class Boss(QueueManager.QueueClient):
	def __init__(self):
		super().__init__()
		
	def post(self):
		size = np.random.randint(300, 3_000)
		a = np.random.rand(size, size)
		b = np.random.rand(size)
		t = Task(a,b,size)
		self.task_queue.put(t)
		
	def get(self):
		print("J'ai reçu un résultat "+str(self.result_queue.get()))
	
	
if __name__=="__main__":
	boss = Boss()
	for i in range(10):
		boss.post()
		
	while(1):
		boss.get()
