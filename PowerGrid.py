import util, sys


class RelayNode:
	def __init__(self, id, parent, children, generators, resources, loads, powerLines, parentPL, childrenPL):
		self.id = id
		self.parent = parent
		self.children = children
		self.generators = generators
		self.loads = loads
		self.resources = resources
		self.powerLines = powerLines
		self.parentPL = parentPL
		self.childrenPL = childrenPL


class Generator:
	def __init__(self, id, maxValue, CO):
		self.id = id
		self.maxValue = maxValue
		self.CO = CO
		self.value = 0


class Resource:
	def __init__(self, id, transitions, environment):
		self.id = id
		self.transitions = transitions
		self.environment = environment
		self.last_generation = 0

	def get_generation(self):
		timePeriod = self.environment.get_time()
		tran = self.transitions[timePeriod]
		dist = {}
		for s in tran:
			if s['from'] == self.last_generation:
				for ns in s['to']:
					dist[ns['to']] = ns['prob']
				break
		
		try:
			ss = self.last_generation
			self.last_generation = util.chooseFromDistribution(dist)
		except Exception as e:
			print 'vvvvvvvvvvvvvvvvvvvvvvvvvvvv'
			print timePeriod, ss, self.last_generation, dist
			print '****************************'
		return self.last_generation