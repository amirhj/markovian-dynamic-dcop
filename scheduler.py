class Scheduler:
	def __init__(self, fg, agents, environment, message_server, opt):
		self.fg = fg
		self.agents = agents
		self.opt = opt
		self.message_server = message_server
		self.environment = environment

	def initialize(self):
		clients = {a:self.agents[a] for a in self.agents}
		self.message_server.load(clients)
		self.message_server.start()

		for a in self.agents:
			self.agents[a].start()

	def run(self):
		print "training..."
		numTimeSteps = 0
		terminate = False
		while not terminate:
			terminate = True
			for a in self.agents:
				if not self.agents[a].converged:
					terminate = False
					break

			if not terminate:
				all_updated = False
				while not all_updated:
					all_updated = True
					for a in self.agents:
						if not self.agents[a].updated:
							all_updated = False
							break

				self.environment.next_time_step()
				for a in self.agents:
					self.agents[a].updated = False

			numTimeSteps += 1

		print "training terminated in", numTimeSteps, "time steps\n"

		# reseting time
		self.environment.reset()
		for r in self.fg.resources:
			self.fg.resources[r].last_generation = 0
		for a in self.agents:
			self.agents[a].training = False
			
		print "testing..."

		for i in range(self.opt['tests']):
			print "%d: " % (i+1,),

			for a in self.agents:
				self.agents[a].updated = False

			all_updated = False
			while not all_updated:
				all_updated = True
				for a in self.agents:
					if not self.agents[a].updated:
						all_updated = False
						break

			all_correct = True
			for a in self.agents:
				if not self.agents[a].tests[-1]:
					all_correct = False
					print "%s:Failed, " % (a,),

			if all_correct:
				print "Good",
			print

			self.environment.next_time_step()

		print 'fert'
		
		for a in self.agents:
			self.agents[a].terminate = True
			print 'waiting for', a
			self.agents[a].join()
			print a, 'joined'

		self.message_server.terminate = True
		print 'waiting for message_server'
		self.message_server.join()
		print 'message_server joined'
	
	def terminate(self):
		pass