import QueueManager
import np
import task

class Boss(QueueManager.QueueClient):
	def __init__(self):
		super()
		self.task = m.task
		self.result = m.result
		
	def post(self):
		size = np.random.randint(300, 3_000)
		a = np.random.rand(size, size)
        	b = np.random.rand(size)
		t = Task(a,b)
		self.task.append(t)
		
	def get(self):
		if(len(result)!=0):
			print("J'ai reçu un résultat "+str(result.pop(0)))
	
	
if __name__=="__main__":
	boss = Boss()
	for i in range(10):
		boss.get()
		
	while(1):
		boss.post()
