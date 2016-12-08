import threading, Queue, time
from util import Counter


class MessageServer(threading.Thread):
	def __init__(self, opt, environment):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.message_queue = Queue.Queue()
		self.print_queue = Queue.Queue()
		self.opt = opt
		self.clients = None
		self.terminate = False
		self.name = 'message-server'
		self.logfile = open('results/log.txt', 'w')
		self.environment = environment
		self.agentLog = {}
		self.timeLog = {}
		self.agentLogTest = {}
		self.timeLogTest = {}
		self.testMode = False
		self.missPrediction = []
		self.missState = []
		self.log_queue = Queue.Queue()
		self.logger = open('logger.txt', 'w')

	
	def load(self, clients):
		self.clients = clients

		for c in self.clients:
			self.agentLog[c] = {t:0 for t in range(self.environment.num_time_steps)}
			self.agentLogTest[c] = {t:0 for t in range(self.environment.num_time_steps)}

		for t in range(self.environment.num_time_steps):
			self.timeLog[t] = {c:0 for c in self.clients}
			self.timeLogTest[t] = {c:0 for c in self.clients}

		
	def run(self):
		while not self.terminate:
			if not self.message_queue.empty():
				m = self.message_queue.get()

				if self.opt['log_messages']:
					self.logfile.write('%d %s\n\n\n' % (self.environment.get_time(), str(m)))

				timeStep = self.environment.get_time()
				if self.testMode:
					self.agentLogTest[m[0]][timeStep] += 1
					self.timeLogTest[timeStep][m[0]] += 1
				else:
					self.agentLog[m[0]][timeStep] += 1
					self.timeLog[timeStep][m[0]] += 1

				self.clients[m[1]].receive(m[0], m[2]) # 0:sender, 2:content
				#time.sleep(2)

			if not self.print_queue.empty():
				c,s = self.print_queue.get()
				if 'Unknown' in c:
					self.missState.append(s)
				if 'Prediction' in c:
					self.missPrediction.append(s)
				print c

			if not self.log_queue.empty():
				c = self.log_queue.get()
				self.logger.write('%s\n' %c)
	
	def send(self, sender, receiver, content, sendtime):
		self.message_queue.put((sender, receiver, content, sendtime))

	def printer(self, c, s):
		self.print_queue.put((c, s))

	def getMisses(self):
		result = {'missPrediction': [a for a in self.missPrediction], 'missState': [a for a in self.missState]}
		del self.missState[:]
		del self.missPrediction[:]
		return result

	def loggger(self, c):
		self.log_queue.put(c)
