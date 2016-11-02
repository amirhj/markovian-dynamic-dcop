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
		self.updated = False
		self.relayNode = self.fg.nodes[self.name]
		self.training = True
		self.evalues = Counter()
		self.counter = Counter()
		self.convergence_queue = PipeQueue(self.opt['convergence_size'])
		self.converged = False
		self.temperature = self.opt['temperature']
		self.tests = []
		self.nextStates = {}
		self.test_log = []
		self.time_states = [set() for t in range(self.environment.num_time_steps+1)]
	
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
			if sender == 'auctioneer':
				if m['type'] == 'submission':
					pass #self.send('auctioneer', {'type':'submission', 'content':self.proposal})
				elif m['type'] == 'result':
					pass #self.update_proposal(m['content']['price'], m['content']['others-actions'], m['content']['in_sellers'], m['content']['in_buyers'])
				elif m['type'] == 'price':
					pass #self.calculate_utility(m['content'])
				elif m['type'] == 'out':
					pass #self.calculate_utility(m['content'])
				else:
					raise Exception('Invalid message type ' + m['type'])
			else:
				raise Exception('Invalid sender '+ sender)

	def process(self):
		if not self.updated:
			old_values = tuple([self.relayNode.resources[r].last_generation for r in self.relayNode.resources])
			new_values = tuple([self.relayNode.resources[r].get_generation() for r in self.relayNode.resources])
			time_step = self.environment.get_time()

			state = (time_step, old_values)
			nstate = (time_step+1, new_values)

			self.time_states[time_step].add(old_values)
			self.time_states[time_step+1].add(new_values)

			if self.training:
				#if not self.converged:
				self.add_transition(state, nstate)

				max_e = 0
				for ns in self.next_states(nstate):
					if max_e < self.evalues[(nstate, ns)]:
						max_e = self.evalues[(nstate, ns)]

				sample = (1 + self.opt['gamma'] * max_e) * self.opt['alpha']
				self.evalues[(state, nstate)] = self.evalues[(state, nstate)] * (1 - self.opt['alpha']) + sample

				self.convergence_queue.push(sum(self.evalues.values()))

				self.converged = False
				if self.convergence_queue.is_full():
					if self.convergence_queue.get_standard_deviation() <= self.opt['standard_deviation']:
						self.converged = True

				self.temperature *= self.opt['decay']
			else:	# test
				found = False
				try:
					probs = self.calculate_probs(state, self.opt['test-temperature'])
					pnstate = chooseFromDistribution(probs)
					found = True
				except Exception as e:
					"""print 'vvvvvvvvvvvvvvvvvvvvvvvvv2'
					print state
					print self.next_states(state)
					print probs
					print '^^^^^^^^^^^^^^^^^^^^^^^^^2'"""
					found = False

				if found:
					self.tests.append(pnstate == nstate)
					self.test_log.append({'pnstate':pnstate[0], 'nstate':nstate[0], 'probes':{s[0]: probs[s] for s in probs}})
				else:
					self.tests.append(False)
					self.test_log.append({'not-found': state[1][0]})

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

	def calculate_probs(self, s, temperature=None):
		if temperature is None:
			temperature = self.temperature

		probs = {}
		b = 0
		for ns in self.next_states(s):
			probs[ns] = 0
			if (s,ns) in self.evalues:
				if self.evalues[(s,ns)] > 0:
					probs[ns] = exp(self.evalues[(s,ns)]/temperature)
					b += probs[ns]

		for ns in probs:
			if b != 0:
				probs[ns] = probs[ns] / b

		return probs