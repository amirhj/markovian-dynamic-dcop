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
		print "training..."
		for i in xrange(self.opt['trains']):
			terminate = False
			while not terminate:
				terminate = True
				for a in self.agents:
					if not self.agents[a].done:
						terminate = False
						break

			print 'time step %d finished' % (i+1,)

			self.environment.next_time_step()
			for a in self.agents:
				self.agents[a].time_end()

		for a in self.agents:
			self.agents[a].converged = True

		print "\n\ntesting..."
		for i in xrange(self.opt['tests']):
			terminate = False
			while not terminate:
				terminate = True
				for a in self.agents:
					if not self.agents[a].done:
						terminate = False
						break

			self.environment.next_time_step()
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

		results = {'nodes': {}, 'times': []}

		for a in self.agents:
			agent = self.agents[a]
			
			results['nodes'][a] = {'intermittent': agent.relayNode.resources[agent.relayNode.resources.keys()[0]].transitions}
			
			results['nodes'][a]['states'] = []
			for t in range(self.environment.num_time_steps):
				states = []
				for s in agent.time_states[t]:
					state = {'from': agent.generations[s], 'to':[]}
					for ns in agent.next_states(s):
						state['to'].append({'to': agent.generations[ns], 'prob':agent.probabilities[(s,ns)]})
					states.append(state)
				results['nodes'][a]['states'].append(states)

			results['nodes'][a]['messages'] = [self.message_server.agentLog[a][t] for t in range(self.environment.num_time_steps)]

		for t in range(self.environment.num_time_steps):
			results['times'][t] = {a:self.message_server.timeLog[t][a] for a in self.agents}

		folder = 'results/'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		os.mkdir(folder)
		os.mkdir(folder+'/evalues')

		res = open(folder+'/result.txt', 'w')
		res.write(json.dumps(result, indent=4))
		res.close()