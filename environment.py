class Environment:
	def __init__(self, num_time_steps):
		self.num_time_steps = num_time_steps
		self.time_count = 0
		self.time_step = 0

	def get_time(self):
		return self.time_step

	def next_time_step(self):
		self.time_count += 1
		ss = self.time_step
		self.time_step = self.time_count % self.num_time_steps

	def reset(self):
		self.time_step = 0