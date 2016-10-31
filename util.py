import math


class PipeQueue:
	def __init__(self, size):
		self.size = size
		self.queue = []

	def push(self, item):
		if len(self.queue) == self.size:
			del self.queue[-1]		
		self.queue.insert(0,item)

	def get(self):
		return self.queue

	def is_full(self):
		return len(self.queue) == self.size

	def get_standard_deviation(self):
		avg = sum(self.queue)/len(self.queue)
		return math.sqrt(sum([(i-avg)**2 for i in self.queue])/len(self.queue))

