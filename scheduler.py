class Scheduler:
	def __init__(self, grid, agents, environment, message_server, opt):
		self.grid = grid
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

		self.auctioneer.start()

	def run(self):
		print "training..."
		numTimeSteps = 0
		terminate = False
		while not terminate:
			all_updated = True
			for a in self.agents:
				if not self.agents[a].updated:
					all_updated = False
					break
			if all_updated:
				self.environment.next_time_step()

			terminate = True
			for a in self.agents:
				if self.agents[a].converged == False:
					terminate = False
					break

			numTimeSteps += 1

		print "training terminated in", numTimeSteps, "time steps\n"

		print "testing..."
		self.environment.reset()
		for i in xrange(self.opt['tests']):
			print "%d: " % (i+1,),
			all_updated = True
			for a in self.agents:
				if not self.agents[a].updated:
					all_updated = False
					break
			if all_updated:
				self.environment.next_time_step()

				all_correct = True
				for a in self.agents:
					if not self.agents[a].tests[-1]:
						all_correct = False
						print "%s:Failed, " % (s,),
				
				if all_correct:
					print "Good",
				print

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