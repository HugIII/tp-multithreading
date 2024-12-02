from multiprocessing.managers import BaseManager
from queue import Queue
from abc import abstractmethod

class QueueManager(BaseManager):
	def __init__(self):
		super().__init__(address=("127.0.0.1",50000),authkey=b'abc')
		self.task_queue = Queue()
		self.result_queue = Queue()
		super().register("task",callable=lambda:task_queue)
		super().register("result",callable=lambda:result_queue)
	
		
class QueueClient:
	def __init__(self):
		self.m = QueueManager()
		self.m.connect()

	@abstractmethod
	def get():
		pass
	
	@abstractmethod
	def post():
		pass
		
if __name__=="__main__":
	m = QueueManager()
	m.start()
	while(1):
		pass
