import threading, Queue
from datetime import datetime
from util import Counter, PipeQueue, chooseFromDistribution
from math import exp

class Agent(threading.Thread):
	def __init__(self, name, fg, environment, message_server, opt):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.message_queue = Queue.Queue()
		self.message_server = message_server
		self.terminate = False
		self.opt = opt
		self.fg = fg
		self.name = name
		self.environment = environment
		self.done = False
		self.relayNode = self.fg.nodes[self.name]
		self.training = True
		self.probabilities = Counter()
		self.transition_counter = Counter()
		self.convergence_queue = PipeQueue(self.opt['convergence_size'])
		self.converged = False
		self.temperature = self.opt['temperature']
		self.tests = []
		self.nextStates = {}
		self.test_log = []
		self.time_states = [set() for t in range(self.environment.num_time_steps+1)]
		self.action_taken_neighbours = []
		self.all_neighbours_took = False
		self.dcopPhase = 0
		self.solvingDCOP = False
		self.dcopMessages = {}
		self.last_state = None
		self.decision_made = False
	
	def run(self):
		while not self.terminate:
			self.read_message()
			self.process()

	def receive(self, sender, content):
		self.message_queue.put((sender, content))
	
	def send(self, receiver, content):
		self.message_server.send(self.name, receiver, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	def read_message(self):
		while not self.message_queue.empty():
			sender, m = self.message_queue.get()
			if m['type'] == 'action-taken':
				self.action_taken_neighbours.append(sender)
				if self.relayNode.num_neighbours == len(self.action_taken_neighbours):
					self.all_neighbours_took = True
					del self.action_taken_neighbours[:]
				else:
					self.all_neighbours_took = False

			elif m['type'] == 'request-for-dcop':
				self.solvingDCOP = True
				for c in self.relayNode.children:
					self.send(c, {'type': 'request-for-dcop'})
				
			elif m['type'] == 'dydop-phase1':
				self.solvingDCOP = True
				self.dcopPhase = 1
				self.dcopMessages[sender] = m['content']

			elif m['type'] == 'dydop-phase2':
				self.solvingDCOP = True
				self.dcopPhase = 2
				self.dcopMessages[sender] = m['content']

			else:
				raise Exception('Invalid message type ' + m['type'])
			self.updated = True

	def add_transition(self, s, ns):
		if s not in self.nextStates:
			self.nextStates[s] = set()
		self.nextStates[s].add(ns)

	def next_states(self, s):
		nextstates = []
		if s in self.nextStates:
			nextstates = list(self.nextStates[s])
		return nextstates

	def calculate_probs(self, s):
		b = 0
		for ns in self.next_states(s):
			self.probabilities[(s,ns)] = self.transition_counter[(s,ns)]
			b += probs[ns]

		for ns in self.next_states(s):
			if b != 0:
				self.probabilities[(s,ns)] = self.probabilities[(s,ns)] / b

	def process(self):
		if self.converged:
			self.make_decision()
		else:
			self.learn_transitions()

		if self.solvingDCOP:
			self.dcop()

		self.check_time_termination()

	def learn_transitions(self):
		if self.dcopPhase == 0:	# Agent is not in DCOP solving mode
			# Start solving DCOP by doing phase1
			self.dcopPhase = 1
			self.solvingDCOP = True
		elif self.dcopPhase == 3:	# Agent solved DCOP
			# Learning transition probabilities
			time_step = self.environment.get_time()
			generators = {g:self.relayNode.generators[g].value for g in self.relayNode.generators}

			powerLines = self.relayNode.get_powerLine_values()
			powerLineValues = tuple([powerLines[pl] for pl in powerLines])
			state = (time_step, powerLineValues)

			self.time_states[time_step].add(state)

			# For the first time in t=0 there is no previous calculated dcop solution
			if self.last_state is not None:
				self.transition_counter[(self.last_state, state)] += 1
				self.add_transition(self.last_state, state)
				self.calculate_probs(self.last_state)


			# Back to no DCOP solving mode
			self.dcopPhase = 0

			self.last_state = state
			self.done = True

	def make_decision(self):
		if not self.decision_made:
			pass

			self.decision_made = True
			for n in self.relayNode.neighbours:
				self.send(n, {'type': 'action-taken'})
		
		# Checking for good decision
		if self.all_neighbours_took:

			# check for goodness
			if good:
				pass
			else:
				# Asking children for solving DCOP
				for c in self.relayNode.children:
					self.send(c, {'type': 'request-for-dcop'})
			

	def time_end(self):
		self.decision_made = False