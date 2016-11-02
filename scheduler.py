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
		self.numTimeSteps = 0
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

			self.numTimeSteps += 1

		print "training terminated in", self.numTimeSteps, "time steps\n"

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
			res = []
			for a in self.agents:
				if not self.agents[a].tests[-1]:
					all_correct = False
					print "%s:Failed, " % (a,),
					res.append(a)

			if all_correct:
				print "Good",
			print

			self.test_log.append(res)

			self.environment.next_time_step()

		#print 'fert'
		
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

		correct = 0
		for t in self.test_log:
			if len(t) == 0:
				correct += 1
		result = {'input-file': sys.argv[1], 'correct': correct, 'options': self.opt, 'tests': [], 'convergence':self.numTimeSteps}

		for i in range(self.opt['tests']):
			res = {'failed': self.test_log[i]}
			if len(self.test_log[i]) > 0:
				res['detatails'] = {}
				for a in self.test_log[i]:
					res['detatails'][a] = self.agents[a].test_log[i]
			result['tests'].append(res)

		print 'Writing results...'
		folder = 'results/'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		os.mkdir(folder)
		os.mkdir(folder+'/evalues')

		res = open(folder+'/result.txt', 'w')
		res.write(json.dumps(result, indent=4))
		res.close()

		for a in self.agents:
			agent = self.agents[a]
			transitions = []
			for t in range(self.environment.num_time_steps):
				time_step = []
				for s in agent.time_states[t]:
					state = {'from': s[0], 'to':[]}
					dis = {}
					for ns in agent.next_states((t, s)):
						dis[ns[1][0]] = agent.evalues[((t,s),ns)]

					probid = self.to_prob(dis)
					for k in probid:
						state['to'].append({'to': k, 'prob': probid[k]})
					time_step.append(state)

				transitions.append(time_step)

			res = open(folder + '/evalues/' + a + '.txt', 'w')
			res.write(json.dumps(transitions, indent=4))
			res.close()

			evalues = {}
			for s in agent.evalues:
				evalues[str(s)] = agent.evalues[s]

			res = open(folder + '/evalues/' + a + '-evalues.txt', 'w')
			res.write(json.dumps(evalues, indent=4))
			res.close()

	def to_prob(self, dis):
		base = sum(dis.values())
		for d in dis:
			dis[d] = dis[d]/base
		return dis