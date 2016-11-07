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

		self.neighbours = [c for c in children]
		self.neighbours.append(parent)
		self.num_neighbours = len(self.neighbours)

	def get_CO_emission(self):
		return sum([self.generators[g].get_CO_emission() for g in self.generators])

	def get_powerLine_values(self):
		values = {parentPL: self.powerLines[parentPL].value * -1}
		for pl in self.childrenPL:
			values[pl] = self.powerLines[pl].value
		return values



class Generator:
	def __init__(self, id, maxValue, CO):
		self.id = id
		self.maxValue = maxValue
		self.CO = CO
		self.value = 0

	def get_CO_emission(self):
		return self.value * self.CO



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



class PowerLine:
	def __init__(self, fromNode, toNode, capacity)
		self.fromNode = fromNode
		self.toNode = toNode
		self.capacity = capacity

		# values are in perspective of parent node
		# if value is blow zero the flow is from parent to current node
		# if value is up zero the flow is from current node to parent		
		self.value = 0