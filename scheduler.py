class Scheduler:
	def __init__(self, grid, agents, auctioneer, message_server, opt):
		self.grid = grid
		self.agents = agents
		self.auctioneer = auctioneer
		self.opt = opt
		self.message_server = message_server

	def initialize(self):
		clients = {a:self.agents[a] for a in self.agents}
		clients['auctioneer'] = self.auctioneer
		self.message_server.load(clients)
		self.message_server.start()

		for a in self.agents:
			self.agents[a].start()

		self.auctioneer.start()

	def run(self):
		terminate = False
		while not terminate:
			terminate = self.auctioneer.converged
		
		print 'fert'
		
		for a in self.agents:
			self.agents[a].terminate = True
			print 'waiting for', a
			self.agents[a].join()
			print a, 'joined'

		self.auctioneer.terminate = True
		print 'waiting for auctioneer'
		self.auctioneer.join()
		print 'auctioneer joined'
		self.message_server.terminate = True
		print 'waiting for message_server'
		self.message_server.join()
		print 'message_server joined'
	
	def terminate(self):
		pass