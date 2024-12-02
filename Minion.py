import QueueManager
import task

class Minion(QueueManager.QueueClient):
	def __init__(self):
		super().__init__()
		self.task = self.m.task
		self.result = self.m.result
	
	def get(self):
		print(self.task)
		if(len(self.task)!=0):
			t = self.task.pop(0)
			x = t.work()
			print("J'ai fini une tache")
			self.post(x)
			
		
	def post(self,x):
		self.result.append(x)
		
		
if __name__=="__main__":
	minion = Minion()
	while(1):
		minion.get()
