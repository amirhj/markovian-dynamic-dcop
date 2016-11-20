import sys, os, json
from datetime import datetime

class Scheduler:
	def __init__(self, fg, agents, environment, message_server, opt):
		self.fg = fg
		self.agents = agents
		self.opt = opt
		self.message_server = message_server
		self.environment = environment
		self.test_log = []

	def initialize(self):
		clients = {a:self.agents[a] for a in self.agents}
		self.message_server.load(clients)
		self.message_server.start()

		for a in self.agents:
			self.agents[a].start()

	def run(self):
		#print "training..."
		for i in xrange(self.opt['trains']):
			for a in self.agents:
				self.agents[a].paused = False

			terminate = False
			while not terminate:
				terminate = True
				for a in self.agents:
					if not self.agents[a].done:
						terminate = False
						break

			for a in self.agents:
				self.agents[a].paused = True

			print 'time step %d finished %d' % (i+1, self.environment.get_time())

			self.environment.next_time_step()
			for r in self.fg.resources:
				self.fg.resources[r].get_generation()
			for a in self.agents:
				self.agents[a].time_end()

		self.message_server.testMode = True

		for a in self.agents:
			self.agents[a].converged = True

		print "\n\ntesting..."
		for i in xrange(self.opt['tests']):
			for a in self.agents:
				self.agents[a].paused = False

			terminate = False
			while not terminate:
				terminate = True
				for a in self.agents:
					if not self.agents[a].done:
						terminate = False
						break

			for a in self.agents:
				self.agents[a].paused = True

			print 'time step %d finished %d' % (i+1, self.environment.get_time())

			self.environment.next_time_step()
			for r in self.fg.resources:
				self.fg.resources[r].get_generation()
			for a in self.agents:
				self.agents[a].time_end()

		
		for a in self.agents:
			self.agents[a].terminate = True
			#print 'waiting for', a
			self.agents[a].join()
			#print a, 'joined'

		self.message_server.terminate = True
		#print 'waiting for message_server'
		self.message_server.join()
		#print 'message_server joined'
	
	def terminate(self):
		sys.stdout.flush()
		sys.stderr.flush()

		print 'Writing results...'

		results = {'agents': {}, 'timeSteps': {'train':[], 'test':[]}}

		for a in self.agents:
			agent = self.agents[a]
			
			results['agents'][a] = {'intermittent': agent.relayNode.resources[agent.relayNode.resources.keys()[0]].transitions}
			
			results['agents'][a]['states'] = []
			for t in range(self.environment.num_time_steps):
				states = []
				for s in agent.time_states[t]:
					state = {'label': agent.generations[s], 'from':str(s), 'to':[]}
					for ns in agent.next_states(s):
						state['to'].append({'to': str(ns), 'prob':agent.probabilities[(s,ns)]})
					states.append(state)
				results['agents'][a]['states'].append(states)

			results['agents'][a]['values'] = []
			for t in range(self.environment.num_time_steps):
				fromStates = {}
				for s in agent.time_states[t]:
					gg = agent.generations[s]
					if gg not in fromStates:
						fromStates[gg] = {}

					for ns in agent.next_states(s):
						gg2 = agent.generations[ns]
						if gg2 not in fromStates[gg]:
							fromStates[gg][gg2] = 0

						fromStates[gg][gg2] += agent.transition_counter[(s,ns)]

				for s in fromStates:
					pp = self.make_percentages(fromStates[s])
					fromStates[s] = pp

				results['agents'][a]['values'].append(fromStates)
					

			results['agents'][a]['messages'] = {}
			results['agents'][a]['messages']['train'] = [self.message_server.agentLog[a][t] for t in range(self.environment.num_time_steps)]
			results['agents'][a]['messages']['test'] = [self.message_server.agentLogTest[a][t] for t in range(self.environment.num_time_steps)]

		for t in range(self.environment.num_time_steps):
			results['timeSteps']['train'].append({a:self.message_server.timeLog[t][a] for a in self.agents})
			results['timeSteps']['test'].append({a:self.message_server.timeLog[t][a] for a in self.agents})

		folder = 'results/'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		os.mkdir(folder)
		#os.mkdir(folder+'/evalues')

		res = open(folder+'/results.json', 'w')
		res.write(json.dumps(results, indent=4))
		res.close()

	def make_percentages(self, cc):
		result = {}
		b = 0
		for r in cc:
			result[r] = cc[r]
			b += cc[r]

		b = float(b)

		for r in cc:
			result[r] = '%.2f' % (result[r] * 100 / b,)

		return result